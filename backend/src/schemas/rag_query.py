from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class RAGQueryBase(BaseModel):
    question: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    chapter_id: Optional[str] = None


class RAGQueryCreate(RAGQueryBase):
    pass


class RAGQueryResponse(BaseModel):
    query_id: str
    response: str
    source_chapters: List[str]
    confidence: float
    timestamp: datetime


class RAGQuery(RAGQueryBase):
    id: str
    response: Optional[str] = None
    context: Optional[str] = None
    accuracy_confidence: Optional[float] = None
    timestamp: datetime
    was_answered: bool

    class Config:
        from_attributes = True