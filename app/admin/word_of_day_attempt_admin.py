from sqladmin import ModelView

from app.models import WordOfDayAttempt


class WordOfDayAttemptAdmin(ModelView, model=WordOfDayAttempt): # type: ignore[call-arg]
    column_list = [WordOfDayAttempt.id, WordOfDayAttempt.word_of_day_id, WordOfDayAttempt.word_of_day, WordOfDayAttempt.attempt]
    column_sortable_list = [WordOfDayAttempt.id, WordOfDayAttempt.word_of_day_id]
