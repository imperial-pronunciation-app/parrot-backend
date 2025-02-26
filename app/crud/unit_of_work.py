from types import TracebackType
from typing import Iterator, Self

from fastapi import Depends
from sqlmodel import Session

from app.crud.attempts_repository import AttemptRepository
from app.crud.basic_lesson_repository import BasicLessonRepository
from app.crud.exercise_attempt_phoneme_repository import ExerciseAttemptPhonemeRepository
from app.crud.exercise_attempt_repository import ExerciseAttemptRepository
from app.crud.exercise_repository import ExerciseRepository
from app.crud.leaderboard_user_repository import LeaderboardUserRepository
from app.crud.lesson_repository import LessonRepository
from app.crud.phoneme_repository import PhonemeRepository
from app.crud.recap_lesson_repository import RecapLessonRepository
from app.crud.recording_repository import RecordingRepository
from app.crud.unit_repository import UnitRepository
from app.crud.user_repository import UserRepository
from app.crud.word_of_day_attempt_repository import WordOfDayAttemptRepository
from app.crud.word_of_day_repository import WordOfDayRepository
from app.crud.word_repository import WordRepository
from app.database import get_session


class UnitOfWork:
    def __init__(self, session: Session = Depends(get_session)) -> None:
        self._session = session
        self.recordings = RecordingRepository(self._session)
        self.leaderboard_users = LeaderboardUserRepository(self._session)
        self.words = WordRepository(self._session)
        self.phonemes = PhonemeRepository(self._session)
        self.users = UserRepository(self._session)
        self.exercises = ExerciseRepository(self._session)
        self.units = UnitRepository(self._session)
        self.recap_lessons = RecapLessonRepository(self._session)
        self.basic_lessons = BasicLessonRepository(self._session)
        self.lessons = LessonRepository(self._session)
        self.attempts = AttemptRepository(self._session)
        self.exercise_attempts = ExerciseAttemptRepository(self._session)
        self.word_of_day_attempts = WordOfDayAttemptRepository(self._session)
        self.word_of_day = WordOfDayRepository(self._session)
        self.exercise_attempt_phonemes = ExerciseAttemptPhonemeRepository(self._session)

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        type_: type[BaseException] | None,
        value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.rollback()

    def commit(self) -> None:
        self._session.commit()

    def rollback(self) -> None:
        self._session.rollback()


def get_unit_of_work(session: Session = Depends(get_session)) -> Iterator[UnitOfWork]:
    with UnitOfWork(session) as uow:
        yield uow
