from typing import Optional

from pydantic import BaseModel

from app.schemas.aligned_phonemes import AlignedPhonemes


class AttemptResponse(BaseModel):
    success: bool
    recording_id: Optional[int]
    score: Optional[int]
    phonemes: Optional[AlignedPhonemes]
    xp_gain: Optional[int]
    xp_streak_boost: Optional[int]

class ExerciseAttemptResponse(AttemptResponse):
    exercise_is_completed: bool