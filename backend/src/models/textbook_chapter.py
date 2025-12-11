from sqlalchemy import Column, String, Integer, DateTime, Text
from sqlalchemy.sql import func
from ..database import Base


class TextbookChapter(Base):
    __tablename__ = "textbook_chapters"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)  # Markdown content of the chapter
    chapter_number = Column(Integer, nullable=False)  # 1-6 for the required chapters
    section_structure = Column(String, nullable=True)  # JSON string for sections
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())