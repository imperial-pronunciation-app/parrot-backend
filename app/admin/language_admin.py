from sqladmin import ModelView

from app.models import Language


class LanguageAdmin(ModelView, model=Language): # type: ignore[call-arg]
    column_list = [Language.id, Language.code, Language.name, Language.is_default, Language.words, Language.units, Language.users]
    column_sortable_list = [Language.id, Language.code, Language.name, Language.is_default]
    column_searchable_list = [Language.code, Language.name]
