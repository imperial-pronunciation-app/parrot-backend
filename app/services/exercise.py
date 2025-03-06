
from app.crud.unit_of_work import UnitOfWork
from app.models.exercise import Exercise
from app.models.user import User
from app.schemas.exercise import ExerciseResponse
from app.services.word import WordService


class ExerciseService:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    def to_response(self, exercise: Exercise, user: User) -> ExerciseResponse:
        return ExerciseResponse(
            id=exercise.id,
            word=WordService(self._uow).to_public_with_phonemes(exercise.word),
            is_completed=self.is_completed_by(exercise, user)
        )

    def is_completed_by(self, exercise: Exercise, user: User) -> bool:
        exercise_attempts = self._uow.exercise_attempts.find_by_user_id_and_exercise_id(user.id, exercise.id)
        if exercise_attempts == []:
            return False
        best_attempt = max(exercise_attempts, key=lambda exercise_attempt: exercise_attempt.attempt.score)
        return best_attempt.attempt.score >= 50 or len(exercise_attempts) > 1
    
    def get_xp_gain(self, exercise: Exercise, user_id: int, score: int) -> int:
        max_score = self._uow.exercise_attempts.max_score_for_exercise(
            user_id=user_id,
            exercise_id=exercise.id
        )

        return max(0, score - max_score)