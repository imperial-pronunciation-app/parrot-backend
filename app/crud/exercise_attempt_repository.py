from typing import List, Optional, Sequence, Tuple

from sqlalchemy import Select
from sqlmodel import Session, col, func, select

from app.crud.generic_repository import GenericRepository
from app.models.attempt import Attempt
from app.models.exercise import Exercise
from app.models.exercise_attempt import ExerciseAttempt
from app.models.exercise_attempt_phoneme_link import ExerciseAttemptPhonemeLink
from app.models.phoneme import Phoneme


class ExerciseAttemptRepository(GenericRepository[ExerciseAttempt]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, ExerciseAttempt)
    
    def find_by_user_id_and_exercise_id(self, user_id: int, exercise_id: int) -> Sequence[ExerciseAttempt]:
        stmt = (
            select(ExerciseAttempt)
            .join(Attempt)
            .where(Attempt.user_id == user_id, ExerciseAttempt.exercise_id == exercise_id)
        )
        return self._session.exec(stmt).all()

    def get_aligned_phonemes(self, exercise_attempt: ExerciseAttempt) -> List[Tuple[Optional[Phoneme], Optional[Phoneme]]]:
        links_query = select(ExerciseAttemptPhonemeLink).where(
            ExerciseAttemptPhonemeLink.exercise_attempt_id == exercise_attempt.id
        )
        links = self._session.exec(links_query).all()
        
        # For each link, fetch the expected and actual phonemes
        phoneme_pairs = []
        for link in links:
            expected_phoneme = None
            actual_phoneme = None
            
            if link.expected_phoneme_id:
                expected_query = select(Phoneme).where(Phoneme.id == link.expected_phoneme_id)
                expected_phoneme = self._session.exec(expected_query).first()
                
            if link.actual_phoneme_id:
                actual_query = select(Phoneme).where(Phoneme.id == link.actual_phoneme_id)
                actual_phoneme = self._session.exec(actual_query).first()
                
            phoneme_pairs.append((expected_phoneme, actual_phoneme))
        
        return phoneme_pairs
    
    def max_score_for_exercise(self, user_id: int, exercise_id: int) -> int:
        stmt: Select = (
            select(func.max(Attempt.score))
            .select_from(ExerciseAttempt)
            .join(Attempt)
            .where(
                Attempt.user_id == user_id,
                ExerciseAttempt.exercise_id == exercise_id
            )
        )

        result = self._session.execute(stmt).scalar()
        return result if result is not None else 0

    def average_max_score_for_lesson(self, user_id: int, lesson_id: int) -> float:
        subquery = (
            select(
                ExerciseAttempt.exercise_id,
                func.max(Attempt.score).label("max_score")
            )
            .join(Exercise)
            .join(Attempt)
            .where(
                Attempt.user_id == user_id,
                Exercise.lesson_id == lesson_id
            )
            .group_by(col(ExerciseAttempt.exercise_id))
            .subquery()
        )

        return self._session.exec(
            select(func.avg(subquery.c.max_score))
        ).first() or 0.0
