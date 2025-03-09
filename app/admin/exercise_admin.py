from sqladmin import ModelView

from app.models import Exercise


class ExerciseAdmin(ModelView, model=Exercise): # type: ignore[call-arg]
    column_list = [Exercise.id, Exercise.lesson_id, Exercise.index, Exercise.word_id, Exercise.lesson, Exercise.word, Exercise.attempts]
    column_sortable_list = [Exercise.id, Exercise.lesson_id, Exercise.index, Exercise.word_id]
