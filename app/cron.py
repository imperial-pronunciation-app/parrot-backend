from contextlib import asynccontextmanager
from typing import AsyncGenerator

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import Depends, FastAPI

from app.crud.unit_of_work import UnitOfWork, get_unit_of_work
from app.services.leaderboard import LeaderboardService
from app.services.user import UserService
from app.services.word_of_day import WordOfDayService


uow: UnitOfWork = Depends(get_unit_of_work)
leaderboard_service = LeaderboardService(uow)
user_service = UserService(uow)
word_of_day_service = WordOfDayService(uow)

scheduler = BackgroundScheduler()
reset_leaderboard_job = scheduler.add_job(
    leaderboard_service.reset_leaderboard, "cron", day_of_week="sun", hour=0, minute=0, timezone="UTC"
)
disable_new_user_boost_job = scheduler.add_job(
    user_service.disable_new_user_boost, "cron", hour=0, minute=0, timezone="UTC"
)
change_word_of_day_job = scheduler.add_job(
    word_of_day_service.change_word_of_day, "cron", hour=0, timezone="UTC"
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Before app startup
    scheduler.start()
    yield

    # After app shutdown
    scheduler.shutdown()
