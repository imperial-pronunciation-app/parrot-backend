import math
from typing import List, Sequence

from app.crud.unit_of_work import UnitOfWork
from app.models.leaderboard_user_link import LeaderboardUserLink, League
from app.models.user import User
from app.redis import LRedis
from app.schemas.leaderboard import LeaderboardEntry, LeaderboardResponse
from app.utils.days import days_until_next_sunday


class LeaderboardService:

    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    def get_global_leaderboard_for_user(self, user: User, top_k: int = 3, user_position_k: int = 2) -> LeaderboardResponse:
        days_until_end = days_until_next_sunday()
        league = user.leaderboard_entry.league

        user_rank = LRedis.rank(league, user.leaderboard_entry.id)

        top_leaderboard_user_ids = LRedis.sorted(league, 0, top_k - 1)
        user_position_leaderboard_user_ids = LRedis.sorted(league, user_rank - user_position_k, user_rank + user_position_k)

        leaders = self._leaderboard_entries_from_leaderboard_user_ids(top_leaderboard_user_ids)
        user_position = self._leaderboard_entries_from_leaderboard_user_ids(user_position_leaderboard_user_ids, user_rank - user_position_k)

        return LeaderboardResponse(
            league=league,
            days_until_end=days_until_end,
            leaders=leaders,
            user_position=user_position
        )
    
    def _leaderboard_entries_from_leaderboard_user_ids(self, leaderboard_user_ids: List[int], starting_rank: int = 0) -> List[LeaderboardEntry]:
        if starting_rank < 0:
            # For example, if a league only has 1 player, the rank should start from 1 not -1
            starting_rank = 0
        return [self._leaderboard_entry_from_leaderboard_user_id_and_rank(user_id, starting_rank + i + 1) for i, user_id in enumerate(leaderboard_user_ids)]
    
    def _leaderboard_entry_from_leaderboard_user_id_and_rank(self, leaderboard_user_id: int, rank: int) -> LeaderboardEntry:
        leaderboard_user = self._uow.leaderboard_users.get_by_id(leaderboard_user_id)
        return LeaderboardEntry(leaderboard_user_id, rank, leaderboard_user.user.email, leaderboard_user.xp)
    
    def set_users_new_league(self, leaderboard_users: Sequence[LeaderboardUserLink], new_league: League) -> Sequence[LeaderboardUserLink]:
        """Should only be used for testing"""
        result = self._set_users_new_league_postgres(leaderboard_users, new_league)
        self._reset_redis()
        return result
    
    def reset_leaderboard(self) -> None:
        self._handle_promotions_and_demotions()
        self._log_carry_forward()
        self._reset_redis()
        self._uow.commit()
    
    def _handle_promotions_and_demotions(self) -> None:
        bronze_promotions = self._get_promotions_for_league(League.BRONZE)
        silver_demotions = self._get_demotions_for_league(League.SILVER)
        silver_promotions = self._get_promotions_for_league(League.SILVER)
        gold_demotions = self._get_demotions_for_league(League.GOLD)
        self._set_users_new_league_postgres(bronze_promotions, League.SILVER)
        self._set_users_new_league_postgres(silver_demotions, League.BRONZE)
        self._set_users_new_league_postgres(silver_promotions, League.GOLD)
        self._set_users_new_league_postgres(gold_demotions, League.SILVER)

    def _get_promotions_for_league(self, league: League) -> Sequence[LeaderboardUserLink]:
        # Get total players in the current league
        league_size = LRedis.size_of(league)
        if league_size == 0:
            return []

        # Calculate top 20% indices
        top_20_cutoff = int(league_size * 0.2) - 1  # Top 20% (highest scores)

        # Get top 20% players for promotion (highest scores)
        promoted_leaderboard_user_ids = LRedis.sorted(league, 0, top_20_cutoff)
        return self._uow.leaderboard_users.get_by_ids(promoted_leaderboard_user_ids)

    def _get_demotions_for_league(self, league: League) -> Sequence[LeaderboardUserLink]:
        # Get total players in the current league
        league_size = LRedis.size_of(league)
        if league_size == 0:
            return []

        # Calculate bottom 20% indices
        bottom_20_cutoff = int(league_size * 0.2) - 1  # Bottom 20% (lowest scores)

        # Get top 20% players for promotion (highest scores)
        demoted_leaderboard_user_ids = LRedis.sorted(league, 0, bottom_20_cutoff, desc=False)
        return self._uow.leaderboard_users.get_by_ids([leaderboard_user_id for leaderboard_user_id in demoted_leaderboard_user_ids])

    def _set_users_new_league_postgres(self, users: Sequence[LeaderboardUserLink], new_league: League) -> Sequence[LeaderboardUserLink]:
        for user in users:
            user.league = new_league
        return self._uow.leaderboard_users.upsert_all(users)

    def _log_carry_forward(self) -> None:
        records = self._uow.leaderboard_users.all()
        for record in records:
            record.xp = int(math.log2(record.xp + 1))
        self._uow.leaderboard_users.upsert_all(records)
    
    def _reset_redis(self) -> None:
        for league in League:
            self._reset_redis_by_league(league)

    def _reset_redis_by_league(self, league: League) -> None:
        LRedis.clear_league(league)
        records = self._uow.leaderboard_users.find_by_league(league)
        LRedis.create_entries_from_users(league, records)
