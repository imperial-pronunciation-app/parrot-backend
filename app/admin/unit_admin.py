from sqladmin import ModelView

from app.models import Unit


class UnitAdmin(ModelView, model=Unit): # type: ignore[call-arg]
    column_list = [Unit.id, Unit.name, Unit.description, Unit.index, Unit.language_id, Unit.language, Unit.lessons]
    column_sortable_list = [Unit.id, Unit.name, Unit.description, Unit.index, Unit.language_id]
    column_searchable_list = [Unit.name, Unit.description]
