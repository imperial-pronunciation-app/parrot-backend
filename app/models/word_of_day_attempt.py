from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from app.models.id_model import IdModel


if TYPE_CHECKING:
    from app.models.attempt import Attempt
    from app.models.word_of_day import WordOfDay


class WordOfDayAttempt(IdModel, table=True):
    id: int = Field(primary_key=True, foreign_key="attempt.id")
    attempt: "Attempt" = Relationship()
    word_of_day_id: int = Field(foreign_key="wordofday.id")
    word_of_day: "WordOfDay" = Relationship(back_populates="word_of_day_attempts")
