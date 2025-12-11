from typing import List, Dict, Any
from sqlalchemy.orm import Session
import uuid
from datetime import datetime
from ..models.rag_query import RAGQuery
from ..schemas.rag_query import RAGQueryCreate
from ..vector_store.qdrant_client import QdrantService
from ..config.settings import settings
import openai
from cachetools import TTLCache


class RAGService:
    def __init__(self, db: Session, qdrant_service: QdrantService):
        self.db = db
        self.qdrant_service = qdrant_service
        # Initialize cache with TTL (time-to-live) of 1 hour, max size 1000 items
        self.cache = TTLCache(maxsize=1000, ttl=3600)

    def query_rag(self, question: str, user_id: str = None, session_id: str = None,
                  chapter_id: str = None) -> Dict[str, Any]:
        """Process a RAG query and return a response"""
        # Create a cache key based on the question and chapter_id
        cache_key = f"{question}:{chapter_id or 'all'}"

        # Check if result exists in cache
        if cache_key in self.cache:
            # Return cached result
            cached_result = self.cache[cache_key]
            return cached_result

        # Validate the question
        if not question or len(question.strip()) == 0:
            raise ValueError("Question cannot be empty")

        if len(question) > 1000:  # Limit question length
            raise ValueError("Question is too long")

        # Generate a unique query ID
        query_id = str(uuid.uuid4())

        # Create a RAGQuery record
        rag_query = RAGQueryCreate(
            id=query_id,
            question=question,
            user_id=user_id,
            session_id=session_id,
            chapter_id=chapter_id
        )

        # Save the query to the database
        db_rag_query = RAGQuery(**rag_query.dict())
        self.db.add(db_rag_query)
        self.db.commit()
        self.db.refresh(db_rag_query)

        # Generate embedding for the question
        try:
            # Note: In a real implementation, you would use embeddings API
            # For now, we'll simulate the process
            query_embedding = self._get_embedding(question)

            # Search for similar content in the vector store
            similar_results = self.qdrant_service.search_similar(
                query_embedding=query_embedding,
                limit=5
            )

            # Apply textbook context filtering
            if chapter_id:
                # Only include results from the specified chapter
                filtered_results = [
                    result for result in similar_results
                    if result.get('payload', {}).get('chapter_id') == chapter_id
                ]
                if filtered_results:
                    similar_results = filtered_results
                else:
                    # If no results from the specified chapter, use the original results
                    # but note that these might be from other chapters
                    pass

            # Get context from the most relevant results
            context = self._extract_context(similar_results)

            # Generate response using the LLM based on context
            response = self._generate_response(question, context)

            # Update the RAGQuery record with the response
            db_rag_query.response = response
            db_rag_query.context = context
            db_rag_query.accuracy_confidence = 0.8  # Assuming 80% confidence
            db_rag_query.was_answered = True
            self.db.commit()

            # Prepare the response
            result = {
                "query_id": query_id,
                "response": response,
                "source_chapters": self._get_source_chapters(similar_results),
                "confidence": 0.8,
                "timestamp": datetime.utcnow()
            }

            # Cache the result
            self.cache[cache_key] = result

            return result

        except Exception as e:
            # Update the RAGQuery record with error info
            db_rag_query.response = f"Error processing query: {str(e)}"
            db_rag_query.was_answered = False
            self.db.commit()

            raise e

    def _get_embedding(self, text: str) -> List[float]:
        """Get embedding for a text using OpenAI API"""
        # In a real implementation, you would call the embeddings API
        # For now, we return a dummy embedding
        # In production, you should use OpenAI's embedding API:
        # response = openai.Embedding.create(
        #     input=text,
        #     model="text-embedding-ada-002"
        # )
        # return response['data'][0]['embedding']
        
        # Returning a dummy embedding for now
        return [0.1] * 1536  # OpenAI embeddings are 1536-dimensional

    def _extract_context(self, similar_results: List[Dict]) -> str:
        """Extract context from similar results"""
        if not similar_results:
            return "No relevant context found in the textbook."
        
        # Combine the top results into a context string
        context_parts = []
        for result in similar_results[:3]:  # Use top 3 results
            payload = result.get('payload', {})
            content = payload.get('content', '')
            if content:
                context_parts.append(content)
        
        return ' '.join(context_parts)

    def _generate_response(self, question: str, context: str) -> str:
        """Generate a response using the LLM based on context"""
        # In a real implementation, you would call the LLM API with the context
        # For now, we return a dummy response
        # In production, you might use something like:
        # response = openai.ChatCompletion.create(
        #     model="gpt-3.5-turbo",
        #     messages=[
        #         {"role": "system", "content": f"Answer based on the following context: {context}"},
        #         {"role": "user", "content": question}
        #     ],
        #     max_tokens=500
        # )
        # return response['choices'][0]['message']['content']
        
        # Returning a dummy response for now
        return f"Based on the textbook content, here's an answer to your question about '{question[:50]}...': This is a simulated response based on the textbook context. In a real implementation, this would be generated by an LLM using the provided context."

    def _get_source_chapters(self, similar_results: List[Dict]) -> List[str]:
        """Extract source chapter IDs from similar results"""
        source_chapters = set()
        for result in similar_results:
            payload = result.get('payload', {})
            chapter_id = payload.get('chapter_id')
            if chapter_id:
                source_chapters.add(chapter_id)
        return list(source_chapters)