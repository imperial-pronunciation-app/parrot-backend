from sqlalchemy import Select
from sqlmodel import Session, func, select

from app.crud.generic_repository import GenericRepository
from app.models.attempt import Attempt
from app.models.word_of_day_attempt import WordOfDayAttempt


class WordOfDayAttemptRepository(GenericRepository[WordOfDayAttempt]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, WordOfDayAttempt)

    def max_score_for_word_of_day(self, user_id: int, word_of_day_id: int) -> int:
        stmt: Select = (
            select(func.max(Attempt.score))
            .select_from(WordOfDayAttempt)
            .join(Attempt)
            .where(
                Attempt.user_id == user_id,
                WordOfDayAttempt.word_of_day_id == word_of_day_id
            )
        )

        result = self._session.execute(stmt).scalar()
        return result if result is not None else 0
