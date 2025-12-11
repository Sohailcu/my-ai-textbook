from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.sql import func
from ..database import Base


class UserSession(Base):
    __tablename__ = "user_sessions"

    session_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, nullable=True)  # Unique user identifier, null for anonymous
    is_authenticated = Column(Boolean, default=False)  # Whether user has logged in
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)
    ip_address = Column(String, nullable=True)  # For rate limiting purposes
    last_accessed_chapter = Column(String, nullable=True)  # Last chapter user was reading