from app.crud.unit_of_work import UnitOfWork
from app.models.word import Word
from app.schemas.word import WordPublicWithPhonemes
from app.services.phoneme import PhonemeService


class WordService:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow
        
    def to_public_with_phonemes(self, word: Word) -> WordPublicWithPhonemes:
        phonemes = self._uow.phonemes.find_phonemes_by_word(word.id)
        phoneme_service = PhonemeService(self._uow)
        return WordPublicWithPhonemes(
            id=word.id,
            text=word.text,
            phonemes=[phoneme_service.to_phoneme_public(p, word.language_id) for p in phonemes]
        )
