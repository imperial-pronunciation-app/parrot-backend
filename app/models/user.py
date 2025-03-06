from datetime import date, datetime
from enum import Enum
from random import choice
from typing import TYPE_CHECKING

from fastapi_users_db_sqlmodel import SQLModelBaseUserDB
from sqlmodel import Field, Relationship

from app.models.id_model import IdModel


if TYPE_CHECKING:
    from app.models.language import Language
    from app.models.leaderboard_user_link import LeaderboardUserLink


class Avatar(str, Enum):
    BLUE = "BLUE"
    YELLOW = "YELLOW"
    PURPLE = "PURPLE"
    PINK = "PINK"
    GREEN = "GREEN"
    MINT = "MINT"
    INDIGO = "INDIGO"
    RED = "RED"
    BROWN = "BROWN"


class User(IdModel, SQLModelBaseUserDB, table=True):
    display_name: str
    login_streak: int = Field(default=1)
    last_login_date: date = Field(default_factory=date.today)
    xp_total: int = Field(default=0)
    level: int = Field(default=1)
    new_user: bool = Field(default=True)
    leaderboard_entry: "LeaderboardUserLink" = Relationship(back_populates="user")
    created_at: datetime = Field(default_factory=datetime.now)
    language_id: int = Field(foreign_key="language.id", default=1) # Overriden in on_after_register
    language: "Language" = Relationship(back_populates="users")
    avatar: Avatar = Field(default_factory=lambda: choice(list(Avatar)))
