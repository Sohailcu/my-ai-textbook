from typing import Optional, List
from sqlalchemy.orm import Session
from ..models.user_preference import UserPreference
from ..schemas.user_preference import UserPreferenceCreate, UserPreferenceUpdate


class UserPreferenceService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_preference(self, user_id: str) -> Optional[UserPreference]:
        """Get user preferences by user ID"""
        return self.db.query(UserPreference).filter(
            UserPreference.user_id == user_id
        ).first()

    def create_user_preference(self, user_preference: UserPreferenceCreate) -> UserPreference:
        """Create user preferences"""
        db_pref = UserPreference(**user_preference.dict())
        self.db.add(db_pref)
        self.db.commit()
        self.db.refresh(db_pref)
        return db_pref

    def update_user_preference(self, user_id: str, update_data: UserPreferenceUpdate) -> Optional[UserPreference]:
        """Update user preferences"""
        db_pref = self.get_user_preference(user_id)
        if db_pref:
            update_dict = update_data.dict(exclude_unset=True)
            for field, value in update_dict.items():
                setattr(db_pref, field, value)
            self.db.commit()
            self.db.refresh(db_pref)
            return db_pref
        return None

    def get_preferred_chapters(self, user_id: str) -> List[int]:
        """Get preferred chapter order for a user"""
        pref = self.get_user_preference(user_id)
        if pref and pref.preferred_chapters:
            import json
            try:
                return json.loads(pref.preferred_chapters)
            except json.JSONDecodeError:
                # Return empty list if JSON parsing fails
                return []
        return []