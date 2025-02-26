# import pytest
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture
from sqlmodel import Session

from app.crud.unit_of_work import UnitOfWork
from app.models.exercise import Exercise
from app.models.lesson import Lesson
from app.models.phoneme import Phoneme
from app.models.unit import Unit
from app.models.word import Word
from app.models.word_of_day import WordOfDay
from app.models.word_phoneme_link import WordPhonemeLink
from app.services.attempts import AttemptService


def test_word_of_day_attempts(
    session: Session, uow: UnitOfWork, mocker: MockerFixture, auth_client: TestClient, sample_word_of_day: WordOfDay
) -> None:
    """Test post_word_of_day_attempt"""

    test_word = "software"
    test_word_phonemes = ["s", "oʊ", "f", "t", "w", "ɛ", "r"]
    similarity = 100
    recording_id = 1
    recording_phonemes = [
        [{"id": 1, "ipa": "s", "respelling": "s"}, {"id": 1, "ipa": "s", "respelling": "s"}],
        [{"id": 2, "ipa": "oʊ", "respelling": "oʊ"}, {"id": 2, "ipa": "oʊ", "respelling": "oʊ"}],
        [{"id": 3, "ipa": "f", "respelling": "f"}, {"id": 3, "ipa": "f", "respelling": "f"}],
        [{"id": 4, "ipa": "t", "respelling": "t"}, {"id": 4, "ipa": "t", "respelling": "t"}],
        [{"id": 5, "ipa": "w", "respelling": "w"}, {"id": 5, "ipa": "w", "respelling": "w"}],
        [{"id": 6, "ipa": "ɛ", "respelling": "ɛ"}, {"id": 6, "ipa": "ɛ", "respelling": "ɛ"}],
        [{"id": 7, "ipa": "r", "respelling": "r"}, {"id": 7, "ipa": "r", "respelling": "r"}],
    ]

    # mock_os_remove = mocker.patch("os.remove")
    mock_service = mocker.Mock(spec=AttemptService)
    mocker.patch("app.routers.attempts.AttemptService", return_value=mock_service)
    phonemes = uow.phonemes.upsert_all([Phoneme(ipa=p, respelling=p) for p in test_word_phonemes])
    mock_service.post_word_of_day_attempt.return_value = {
        "score": similarity,
        "xp_gain": 1.5 * similarity,
        "recording_id": recording_id,
        "phonemes": recording_phonemes,
    }

    word = uow.words.upsert(Word(text=test_word))
    phonemes = uow.phonemes.upsert_all([Phoneme(ipa=p, respelling=p) for p in test_word_phonemes])
    session.add_all([WordPhonemeLink(word_id=word.id, phoneme_id=p.id, index=i) for i, p in enumerate(phonemes)])
    session.commit()
    unit = uow.units.upsert(Unit(name="test", description="test", order=1))
    lesson = uow.lessons.upsert(Lesson(title="test", unit_id=unit.id, order=1))
    uow.exercises.upsert(Exercise(lesson_id=lesson.id, word_id=word.id, index=0))
    uow.commit()

    wav_file_path = f"tests/assets/{test_word}.wav"
    with open(wav_file_path, "rb") as f:
        files = {"audio_file": f}

        recording_response = auth_client.post("/api/v1/word_of_day", files=files)
    assert recording_response.status_code == 200
    data = recording_response.json()
    assert data["score"] == similarity
    assert data["xp_gain"] == 1.5 * similarity
    assert data["recording_id"] == recording_id

    mock_service.post_word_of_day_attempt.assert_called_once()
