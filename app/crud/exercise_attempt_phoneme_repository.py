from typing import Sequence

from sqlmodel import Session

from app.models.exercise_attempt_phoneme_link import ExerciseAttemptPhonemeLink

        
class ExerciseAttemptPhonemeRepository():

    def __init__(self, session: Session) -> None:
        self._session = session

    def upsert(self, record: ExerciseAttemptPhonemeLink) -> ExerciseAttemptPhonemeLink:
        self._session.add(record)
        self._session.flush()
        self._session.refresh(record)
        return record

    def upsert_all(self, records: Sequence[ExerciseAttemptPhonemeLink]) -> Sequence[ExerciseAttemptPhonemeLink]:
        self._session.add_all(records)
        self._session.flush()
        for record in records:
            self._session.refresh(record)
        return records
