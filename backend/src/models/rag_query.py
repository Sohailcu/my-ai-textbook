from sqlalchemy import Column, String, Integer, DateTime, Text, Float, Boolean, ForeignKey
from sqlalchemy.sql import func
from ..database import Base


class RAGQuery(Base):
    __tablename__ = "rag_queries"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, nullable=True)  # Optional, for authenticated users
    question = Column(Text, nullable=False)  # User's question text
    response = Column(Text, nullable=False)  # AI-generated response
    context = Column(Text, nullable=True)  # Textbook content used to generate response
    accuracy_confidence = Column(Float, nullable=True)  # 0-1, confidence level in response accuracy
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    was_answered = Column(Boolean, default=False)  # Whether AI provided a response based on textbook content
    chapter_id = Column(String, ForeignKey("textbook_chapters.id"), nullable=True)