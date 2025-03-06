from datetime import date, timedelta
from typing import Tuple

from app.crud.unit_of_work import UnitOfWork
from app.models.leaderboard_user_link import LeaderboardUserLink
from app.models.user import User
from app.redis import LRedis


class UserService:

    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    def update_xp_with_boost(
        self,
        user: User,
        lesson_xp: int,
        login_streak_boost_factor: float = 0.1,
        login_streak_boost_max: float = 0.5,
        new_user_boost_factor: float = 1.5
    ) -> Tuple[int, int]:
        """Returns the XP gained including boosts"""
        assert lesson_xp >= 0
        xp_gain_float = float(lesson_xp)
        login_streak_boost = xp_gain_float * min((user.login_streak - 1) * login_streak_boost_factor, login_streak_boost_max)
        if user.new_user:
            xp_gain_float *= new_user_boost_factor
        original_xp_gain = xp_gain_float
        xp_gain_float += login_streak_boost
        xp_gain = int(xp_gain_float)

        entry = user.leaderboard_entry
        entry.xp += xp_gain
        self._uow.leaderboard_users.upsert(entry)
        user.xp_total += xp_gain
        self._uow.users.upsert(user)
        self._uow.commit()
        LRedis.update_xp(entry.league, entry.id, xp_gain)
        return int(original_xp_gain), int(login_streak_boost)

    def update_xp(self, user: User, xp_gain: int) -> LeaderboardUserLink:
        """Should be used for testing only, as it does not account for boosts, e.g. streaks"""
        assert xp_gain >= 0
        entry = user.leaderboard_entry
        entry.xp += xp_gain
        entry = self._uow.leaderboard_users.upsert(entry)
        user.xp_total += xp_gain
        self._uow.users.upsert(user)
        self._uow.commit()
        LRedis.update_xp(entry.league, entry.id, xp_gain)
        return entry

    def update_login_streak(self, user: User) -> User:
        today = date.today()
        datediff = today - user.last_login_date
        match datediff.days:
            case 0:
                pass
            case 1:
                user.login_streak += 1
            case _:
                user.login_streak = 1
        user.last_login_date = today
        user = self._uow.users.upsert(user)
        self._uow.commit()
        return user

    def disable_new_user_boost(self, boost_duration_days: int = 3) -> None:
        users = self._uow.users.find_by_new_users_created_before(date.today() - timedelta(days=boost_duration_days))
        for user in users:
            user.new_user = False
        self._uow.users.upsert_all(users)
        self._uow.commit()
