from sqladmin import ModelView

from app.models import RecapLesson


class RecapLessonAdmin(ModelView, model=RecapLesson): # type: ignore[call-arg]
    column_list = [RecapLesson.id, RecapLesson.user_id, RecapLesson.unit_id, RecapLesson.unit]
    column_sortable_list = [RecapLesson.id, RecapLesson.user_id, RecapLesson.unit_id]
