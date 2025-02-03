from dataclasses import dataclass
from typing import List

from pydantic import BaseModel

from app.models.leaderboard_user import League


@dataclass
class LeaderboardEntry:
    rank: int
    username: str
    xp: int


class LeaderboardResponse(BaseModel):
    league: League
    days_until_end: int
    leaders: List[LeaderboardEntry]
    current: List[LeaderboardEntry]
