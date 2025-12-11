from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..services.textbook_service import TextbookService
from ..schemas.textbook_chapter import TextbookChapter


router = APIRouter()


@router.get("/textbook/chapters", response_model=List[TextbookChapter])
def get_textbook_chapters(db: Session = Depends(get_db)):
    """Get all textbook chapters"""
    service = TextbookService(db)
    return service.get_chapters()


@router.get("/textbook/chapters/structured")
def get_textbook_chapters_structured(db: Session = Depends(get_db)):
    """Get all textbook chapters with section structure"""
    service = TextbookService(db)
    return service.get_chapters_with_structure()


@router.get("/textbook/chapter/{chapter_id}", response_model=TextbookChapter)
def get_textbook_chapter(chapter_id: str, db: Session = Depends(get_db)):
    """Get a specific textbook chapter by ID"""
    service = TextbookService(db)
    chapter = service.get_chapter(chapter_id)
    
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")
    
    return chapter