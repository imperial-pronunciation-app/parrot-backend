from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship

from app.models.id_model import IdModel


if TYPE_CHECKING:
    from app.models.attempt import Attempt
    from app.models.lesson import Lesson
    from app.models.word import Word

class Exercise(IdModel, table=True):
    lesson_id: int = Field(foreign_key="lesson.id")
    lesson: "Lesson" = Relationship(back_populates="exercises")
    index: int
    word_id: int = Field(foreign_key="word.id")
    word: "Word" = Relationship(back_populates="exercises")
    attempts: List["Attempt"] = Relationship(back_populates="exercise", cascade_delete=True)

    def previous_exercise(self) -> Optional["Exercise"]:
        """Returns the previous exercise within the lesson, or None if it's the first exercise."""
        return self.lesson.exercises[self.index - 1] if self.index > 0 else None

    def next_exercise(self) -> Optional["Exercise"]:
        """Returns the next exercise within the lesson, or None if it's the last exercise."""
        return self.lesson.exercises[self.index + 1] if self.index < len(self.lesson.exercises) - 1 else None
