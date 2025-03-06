from typing import List

from pydantic import BaseModel

from app.models.leaderboard_user_link import League
from app.models.user import Avatar


class LeaderboardEntry(BaseModel):
    id: int
    rank: int
    display_name: str
    xp: int
    avatar: Avatar


class LeaderboardResponse(BaseModel):
    league: League
    days_until_end: int
    leaders: List[LeaderboardEntry]
    user_position: List[LeaderboardEntry]
