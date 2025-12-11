from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Optional, Dict, Any
from ..config.settings import settings


class QdrantService:
    def __init__(self):
        self.client = QdrantClient(
            host=settings.qdrant_host,
            port=settings.qdrant_port,
            api_key=settings.qdrant_api_key,
        )
        
        # Collection name for textbook embeddings
        self.collection_name = "textbook_embeddings"
        
        # Initialize the collection if it doesn't exist
        self._init_collection()
    
    def _init_collection(self):
        """Initialize the Qdrant collection if it doesn't exist"""
        try:
            # Check if collection exists
            self.client.get_collection(self.collection_name)
        except:
            # Create collection if it doesn't exist
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=1536,  # Default size for OpenAI embeddings
                    distance=models.Distance.COSINE
                )
            )
    
    def add_embeddings(self, 
                      ids: List[str], 
                      embeddings: List[List[float]], 
                      payloads: List[Dict[str, Any]]):
        """Add embeddings to the collection"""
        self.client.upsert(
            collection_name=self.collection_name,
            points=models.Batch(
                ids=ids,
                vectors=embeddings,
                payloads=payloads
            )
        )
    
    def search_similar(self, 
                      query_embedding: List[float], 
                      limit: int = 10) -> List[Dict[str, Any]]:
        """Search for similar embeddings"""
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=limit
        )
        
        return [
            {
                "id": result.id,
                "payload": result.payload,
                "score": result.score
            }
            for result in results
        ]
    
    def delete_by_payload(self, key: str, value: Any):
        """Delete points based on payload value"""
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=models.FilterSelector(
                filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key=key,
                            match=models.MatchValue(value=value)
                        )
                    ]
                )
            )
        )