from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.sql import func
from ..database import Base


class UserPreference(Base):
    __tablename__ = "user_preferences"

    user_id = Column(String, primary_key=True, index=True)
    language = Column(String(10), default='en')  # Default 'en', optional 'ur' for Urdu
    personalization_enabled = Column(Boolean, default=True)  # Whether personalization features are on
    preferred_chapters = Column(String, nullable=True)  # JSON string: order of preference for chapter recommendations
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())