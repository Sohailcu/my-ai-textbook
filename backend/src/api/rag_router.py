from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any
from ..database import get_db
from ..vector_store.qdrant_client import QdrantService
from ..services.rag_service import RAGService
from ..schemas.rag_query import RAGQueryCreate


router = APIRouter()


@router.post("/rag/query")
def query_rag_endpoint(
    query: RAGQueryCreate,
    db: Session = Depends(get_db),
    qdrant_service: QdrantService = Depends(QdrantService)
):
    """Endpoint to submit a question to the RAG system"""
    try:
        rag_service = RAGService(db, qdrant_service)
        result = rag_service.query_rag(
            question=query.question,
            user_id=query.user_id,
            session_id=query.session_id,
            chapter_id=query.chapter_id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing RAG query: {str(e)}")