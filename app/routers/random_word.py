import random

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models import Word
from app.schemas.random_word import RandomWord


router = APIRouter()


@router.get("/api/v1/random_word", response_model=RandomWord)
async def get_random_word(session: Session = Depends(get_session)) -> RandomWord:
    query = select(Word)
    words = session.exec(query).all()
    if not words:
        raise HTTPException(status_code=404, detail="No words found")

    random_word = random.choice(words)

    # # TODO: Return associated phonemes
    # word_phoneme_entries = db.exec(
    #     select(WordPhonemes).filter(WordPhonemes.word_id == random_word.id).order_by(WordPhonemes.index)
    # ).all()
    # phoneme_ids = [entry.phoneme_id for entry in word_phoneme_entries]
    # word_phonemes = db.exec(select(Phoneme).filter(Phoneme.id.in_(phoneme_ids))).all()
    # word_phonemes = [
    #     WordPhoneme(phoneme_id=phoneme.id, ipa=phoneme.ipa, respelling=phoneme.respelling) for phoneme in word_phonemes
    # ]

    assert random_word.id is not None
    return RandomWord(word_id=random_word.id, word=random_word.word, word_phonemes=[])
