from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserSessionBase(BaseModel):
    session_id: str
    user_id: Optional[str] = None
    is_authenticated: bool = False
    ip_address: Optional[str] = None


class UserSessionCreate(UserSessionBase):
    pass


class UserSession(UserSessionBase):
    created_at: datetime
    expires_at: Optional[datetime] = None
    last_accessed_chapter: Optional[str] = None

    class Config:
        from_attributes = True