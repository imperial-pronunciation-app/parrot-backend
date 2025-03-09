from sqladmin import ModelView

from app.models import ExerciseAttemptPhonemeLink


class ExerciseAttemptPhonemeLinkAdmin(ModelView, model=ExerciseAttemptPhonemeLink): # type: ignore[call-arg]
    column_list = [
        ExerciseAttemptPhonemeLink.exercise_attempt_id,
        ExerciseAttemptPhonemeLink.expected_phoneme_id,
        ExerciseAttemptPhonemeLink.actual_phoneme_id,
        ExerciseAttemptPhonemeLink.index
    ]
    column_sortable_list = [
        ExerciseAttemptPhonemeLink.exercise_attempt_id,
        ExerciseAttemptPhonemeLink.expected_phoneme_id,
        ExerciseAttemptPhonemeLink.actual_phoneme_id,
        ExerciseAttemptPhonemeLink.index
    ]
