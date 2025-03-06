from typing import Optional

from fastapi_users import schemas
from pydantic import BaseModel

from app.models.language import Language
from app.models.leaderboard_user_link import League
from app.models.user import Avatar


class UserCreate(schemas.BaseUserCreate):
    display_name: str


class UserUpdate(schemas.BaseUserUpdate):
    display_name: Optional[str] = None
    language_id: Optional[int] = None
    avatar: Optional[Avatar] = None


class UserDetails(BaseModel):
    id: int
    login_streak: int
    xp_total: int
    email: str
    display_name: str
    language: Language
    league: League
    avatar: Avatar
