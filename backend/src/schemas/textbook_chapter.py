from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class TextbookChapterBase(BaseModel):
    title: str
    content: str
    chapter_number: int
    section_structure: Optional[str] = None


class TextbookChapterCreate(TextbookChapterBase):
    pass


class TextbookChapterUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    chapter_number: Optional[int] = None
    section_structure: Optional[str] = None


class TextbookChapter(TextbookChapterBase):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True