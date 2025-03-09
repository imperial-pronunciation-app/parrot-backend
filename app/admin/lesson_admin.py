from sqladmin import ModelView

from app.models import Lesson


class LessonAdmin(ModelView, model=Lesson): # type: ignore[call-arg]
    column_list = [Lesson.id, Lesson.title, Lesson.exercises]
    column_sortable_list = [Lesson.id, Lesson.title]
    column_searchable_list = [Lesson.id, Lesson.title]
