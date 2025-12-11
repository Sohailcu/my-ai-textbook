from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from ..models.user_session import UserSession
from ..schemas.user_session import UserSessionCreate
from ..utils.auth import verify_password, get_password_hash, create_access_token, verify_token


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def create_session(self, user_id: Optional[str] = None, ip_address: Optional[str] = None) -> UserSession:
        """Create a new user session"""
        from ..config.settings import settings
        
        session_id = f"session_{datetime.utcnow().timestamp()}"
        expires_at = datetime.utcnow() + timedelta(days=7)  # Session expires in 7 days
        
        # Create new session
        user_session = UserSession(
            session_id=session_id,
            user_id=user_id,
            is_authenticated=user_id is not None,
            ip_address=ip_address,
            expires_at=expires_at
        )
        
        self.db.add(user_session)
        self.db.commit()
        self.db.refresh(user_session)
        
        return user_session

    def get_session(self, session_id: str) -> Optional[UserSession]:
        """Get a user session by ID"""
        return self.db.query(UserSession).filter(
            UserSession.session_id == session_id
        ).first()

    def update_last_accessed_chapter(self, session_id: str, chapter_id: str) -> bool:
        """Update the last accessed chapter for a session"""
        user_session = self.get_session(session_id)
        if user_session:
            user_session.last_accessed_chapter = chapter_id
            self.db.commit()
            return True
        return False

    def verify_token(self, token: str) -> Optional[str]:
        """Verify a JWT token and return the user ID"""
        try:
            from ..utils.auth import verify_token as token_verifier
            return token_verifier(token)
        except Exception:
            return None