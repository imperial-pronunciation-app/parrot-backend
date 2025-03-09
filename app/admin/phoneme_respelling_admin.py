from sqladmin import ModelView

from app.models import PhonemeRespelling


class PhonemeRespellingAdmin(ModelView, model=PhonemeRespelling): # type: ignore[call-arg]
    column_list = [PhonemeRespelling.phoneme_id, PhonemeRespelling.language_id, PhonemeRespelling.respelling, PhonemeRespelling.phoneme]
    column_sortable_list = [PhonemeRespelling.phoneme_id, PhonemeRespelling.language_id, PhonemeRespelling.respelling]
    column_searchable_list = [PhonemeRespelling.phoneme_id, PhonemeRespelling.language_id, PhonemeRespelling.respelling]
