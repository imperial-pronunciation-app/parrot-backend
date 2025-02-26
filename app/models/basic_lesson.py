from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from app.models.id_model import IdModel


if TYPE_CHECKING:
    from app.models.unit import Unit


class BasicLesson(IdModel, table=True):
    id: int = Field(primary_key=True, foreign_key="lesson.id")
    index: int
    unit_id: int = Field(foreign_key="unit.id")
    unit: "Unit" = Relationship(back_populates="lessons")