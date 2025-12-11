from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.user_preference_service import UserPreferenceService
from ..utils.auth import verify_token
from ..schemas.user_preference import UserPreferenceUpdate


router = APIRouter()
security = HTTPBearer()


@router.get("/user/preferences")
def get_user_preferences(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get user preferences (requires authentication)"""
    user_id = verify_token(credentials.credentials)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
    
    service = UserPreferenceService(db)
    preferences = service.get_user_preference(user_id)
    
    if not preferences:
        # If no preferences exist, return default values
        return {
            "language": "en",
            "personalization_enabled": True,
            "preferred_chapters": [],
            "created_at": None,
            "updated_at": None
        }
    
    return preferences


@router.put("/user/preferences")
def update_user_preferences(
    update_data: UserPreferenceUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Update user preferences (requires authentication)"""
    user_id = verify_token(credentials.credentials)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
    
    service = UserPreferenceService(db)
    updated_preferences = service.update_user_preference(user_id, update_data)
    
    if not updated_preferences:
        # If preferences don't exist, create them
        from ..schemas.user_preference import UserPreferenceCreate
        new_preferences = UserPreferenceCreate(
            user_id=user_id,
            language=update_data.language or 'en',
            personalization_enabled=update_data.personalization_enabled or True,
            preferred_chapters=update_data.preferred_chapters
        )
        updated_preferences = service.create_user_preference(new_preferences)
    
    return {
        "success": True,
        "message": "Preferences updated successfully"
    }