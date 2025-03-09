from sqladmin import ModelView

from app.models import BasicLesson


class BasicLessonAdmin(ModelView, model=BasicLesson): # type: ignore[call-arg]
    column_list = [BasicLesson.id, BasicLesson.index, BasicLesson.unit_id, BasicLesson.unit]
    column_sortable_list = [BasicLesson.id, BasicLesson.index, BasicLesson.unit_id]
