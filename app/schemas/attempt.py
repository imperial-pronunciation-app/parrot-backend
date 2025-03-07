from typing import Optional

from pydantic import BaseModel

from app.schemas.aligned_phonemes import AlignedPhonemes


class AttemptFeedback(BaseModel):
    recording_id: int
    score: int
    phonemes: AlignedPhonemes
    xp_gain: int
    xp_streak_boost: int
class AttemptResponse(BaseModel):
    success: bool
    feedback: Optional[AttemptFeedback]

class ExerciseAttemptResponse(AttemptResponse):
    exercise_is_completed: bool