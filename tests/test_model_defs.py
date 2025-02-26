from sqlmodel import SQLModel, create_engine

from app.models.attempt import Attempt  # noqa: F401
from app.models.basic_lesson import BasicLesson  # noqa: F401
from app.models.exercise import Exercise  # noqa: F401
from app.models.exercise_attempt import ExerciseAttempt  # noqa: F401
from app.models.exercise_attempt_phoneme_link import ExerciseAttemptPhonemeLink  # noqa: F401
from app.models.leaderboard_user_link import LeaderboardUserLink  # noqa: F401
from app.models.lesson import Lesson  # noqa: F401
from app.models.phoneme import Phoneme  # noqa: F401
from app.models.recap_lesson import RecapLesson  # noqa: F401
from app.models.recording import Recording  # noqa: F401
from app.models.unit import Unit  # noqa: F401
from app.models.user import User  # noqa: F401
from app.models.word import Word  # noqa: F401
from app.models.word_of_day import WordOfDay  # noqa: F401
from app.models.word_of_day_attempt import WordOfDayAttempt  # noqa: F401
from app.models.word_phoneme_link import WordPhonemeLink  # noqa: F401


def test_create_database() -> None:
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)
    assert True

