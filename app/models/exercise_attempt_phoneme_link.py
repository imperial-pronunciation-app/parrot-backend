from typing import Optional

from sqlmodel import Field, SQLModel


class ExerciseAttemptPhonemeLink(SQLModel, table=True):
  """Links up exercise attempts to phonemes the user found challenging in them
  weight refers to how "badly" the user performed, can be scaled by occurrences of some matching metric
  """
  exercise_attempt_id: Optional[int] = Field(foreign_key="exerciseattempt.id", primary_key=True)
  expected_phoneme_id: Optional[int] = Field(foreign_key="phoneme.id")
  actual_phoneme_id: Optional[int] = Field(foreign_key="phoneme.id")
  index: int = Field(primary_key=True)
