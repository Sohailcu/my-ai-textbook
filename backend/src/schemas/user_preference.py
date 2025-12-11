from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class UserPreferenceBase(BaseModel):
    user_id: str
    language: str = 'en'
    personalization_enabled: bool = True
    preferred_chapters: Optional[str] = None  # JSON string


class UserPreferenceCreate(UserPreferenceBase):
    pass


class UserPreferenceUpdate(BaseModel):
    language: Optional[str] = None
    personalization_enabled: Optional[bool] = None
    preferred_chapters: Optional[str] = None


class UserPreference(UserPreferenceBase):
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True