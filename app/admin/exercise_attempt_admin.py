from sqladmin import ModelView

from app.models import ExerciseAttempt


class ExerciseAttemptAdmin(ModelView, model=ExerciseAttempt): # type: ignore[call-arg]
    column_list = [ExerciseAttempt.id, ExerciseAttempt.exercise_id, ExerciseAttempt.exercise, ExerciseAttempt.attempt]
    column_sortable_list = [ExerciseAttempt.id, ExerciseAttempt.exercise_id]
