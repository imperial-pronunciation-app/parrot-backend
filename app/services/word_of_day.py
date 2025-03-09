from app.crud.unit_of_work import UnitOfWork
from app.models.word_of_day import WordOfDay


class WordOfDayService:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    def change_word_of_day(self) -> None:
        languages = self._uow.languages.all()
        for language in languages:
            word = self._uow.words.get_word_not_used_for(days=365, language=language)
            self._uow.word_of_day.add_word_of_day(word_id=word.id)
            self._uow.words.update_date_of_word_last_used(word=word)
        self._uow.commit()

    def get_xp_gain(self, word_of_day: WordOfDay, user_id: int, score: int) -> int:
        max_score = self._uow.word_of_day_attempts.max_score_for_word_of_day(
            user_id=user_id,
            word_of_day_id=word_of_day.id
        )

        return max(0, score - max_score)
