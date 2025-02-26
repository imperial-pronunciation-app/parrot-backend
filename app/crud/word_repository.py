from datetime import date, timedelta
from random import choice
from typing import Sequence

from sqlmodel import Session, select

from app.crud.generic_repository import GenericRepository
from app.models.phoneme import Phoneme
from app.models.word import Word


class WordRepository(GenericRepository[Word]):
    def __init__(self, session: Session):
        super().__init__(session, Word)

    def get_word_not_used_for(self, days: int) -> Word:
        stmt = select(Word).where(Word.word_of_day_last_used < date.today() - timedelta(days=days))
        res_list = self._session.exec(stmt).all()
        return choice(res_list)

    def update_date_of_word_last_used(self, word: Word, _date: date = date.today()) -> None:
        word.word_of_day_last_used = _date
        self.upsert(word)
    
    def find_with_phoneme(self, phoneme: Phoneme) -> Sequence[Word]:
        stmt = select(Word).join(Phoneme).where(Phoneme.id == phoneme.id)
        return self._session.exec(stmt).all()
