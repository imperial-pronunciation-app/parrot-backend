from typing import List, Optional

from pydantic import BaseModel


class Feedback(BaseModel):
    words: Optional[List[str]]
    phonemes: List[str]

class PronunciationInferenceResponse(BaseModel):
    success: bool
    feedback: Optional[Feedback]