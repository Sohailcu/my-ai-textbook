from typing import List, Optional
from sqlalchemy.orm import Session
from ..models.textbook_chapter import TextbookChapter
from ..schemas.textbook_chapter import TextbookChapterCreate, TextbookChapterUpdate


class TextbookService:
    def __init__(self, db: Session):
        self.db = db

    def get_chapter(self, chapter_id: str) -> Optional[TextbookChapter]:
        """Get a specific textbook chapter by ID"""
        return self.db.query(TextbookChapter).filter(TextbookChapter.id == chapter_id).first()

    def get_chapters(self) -> List[TextbookChapter]:
        """Get all textbook chapters"""
        return self.db.query(TextbookChapter).order_by(TextbookChapter.chapter_number).all()

    def get_chapter_by_number(self, chapter_number: int) -> Optional[TextbookChapter]:
        """Get a textbook chapter by chapter number"""
        return self.db.query(TextbookChapter).filter(TextbookChapter.chapter_number == chapter_number).first()

    def get_chapters_with_structure(self) -> List[dict]:
        """Get all textbook chapters with their section structure"""
        chapters = self.db.query(TextbookChapter).order_by(TextbookChapter.chapter_number).all()
        result = []

        for chapter in chapters:
            chapter_dict = {
                "id": chapter.id,
                "title": chapter.title,
                "chapter_number": chapter.chapter_number,
            }

            # Parse section structure if it exists
            if chapter.section_structure:
                import json
                try:
                    chapter_dict["sections"] = json.loads(chapter.section_structure)
                except json.JSONDecodeError:
                    # If JSON parsing fails, try a simple extraction from content
                    chapter_dict["sections"] = self._extract_sections_from_content(chapter.content)
            else:
                # Extract sections from Markdown content
                chapter_dict["sections"] = self._extract_sections_from_content(chapter.content)

            result.append(chapter_dict)

        return result

    def _extract_sections_from_content(self, content: str) -> List[str]:
        """Extract section titles from Markdown content"""
        import re
        # Find all heading patterns in Markdown (#, ##, ###, etc.)
        headings = re.findall(r'^(#+)\s+(.+)$', content, re.MULTILINE)
        sections = []

        for level, title in headings:
            # Only include main sections (## and ##), not subsections (###, ####, etc.)
            if len(level) <= 3:
                sections.append(title.strip())

        return sections

    def get_recommended_chapters(self, user_id: str) -> List[TextbookChapter]:
        """Get chapter recommendations based on user preferences"""
        # Get user preferences to determine preferred chapters order
        pref_service = UserPreferenceService(self.db)
        pref = pref_service.get_user_preference(user_id)

        if not pref or not pref.preferred_chapters:
            # If no preferences, return all chapters in default order
            return self.get_chapters()

        try:
            # Parse the preferred chapters from JSON
            import json
            preferred_chapter_ids = json.loads(pref.preferred_chapters)
        except (json.JSONDecodeError, TypeError):
            # If JSON parsing fails, return all chapters in default order
            return self.get_chapters()

        # Get chapters in the preferred order
        ordered_chapters = []
        for chapter_id in preferred_chapter_ids:
            chapter = self.get_chapter(chapter_id)
            if chapter:
                ordered_chapters.append(chapter)

        # Add any remaining chapters that weren't specified in preferences
        all_chapters = self.get_chapters()
        remaining_chapters = [ch for ch in all_chapters if ch.id not in preferred_chapter_ids]

        return ordered_chapters + remaining_chapters

    def create_chapter(self, chapter: TextbookChapterCreate) -> TextbookChapter:
        """Create a new textbook chapter"""
        db_chapter = TextbookChapter(**chapter.dict())
        self.db.add(db_chapter)
        self.db.commit()
        self.db.refresh(db_chapter)
        return db_chapter

    def update_chapter(self, chapter_id: str, chapter_update: TextbookChapterUpdate) -> Optional[TextbookChapter]:
        """Update a textbook chapter"""
        db_chapter = self.get_chapter(chapter_id)
        if db_chapter:
            update_data = chapter_update.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_chapter, field, value)
            self.db.commit()
            self.db.refresh(db_chapter)
        return db_chapter

    def delete_chapter(self, chapter_id: str) -> bool:
        """Delete a textbook chapter"""
        db_chapter = self.get_chapter(chapter_id)
        if db_chapter:
            self.db.delete(db_chapter)
            self.db.commit()
            return True
        return False