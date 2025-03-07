from typing import List, Optional

from pydantic import BaseModel


class PronunciationInferenceResponse(BaseModel):
    words: Optional[List[str]]
    phonemes: List[str]
    success: bool
