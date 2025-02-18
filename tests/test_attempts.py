import pytest
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture
from sqlmodel import Session

from app.crud.unit_of_work import UnitOfWork
from app.models.exercise import Exercise
from app.models.lesson import Lesson
from app.models.phoneme import Phoneme
from app.models.unit import Unit
from app.models.word import Word
from app.models.word_phoneme_link import WordPhonemeLink
from app.services.attempts import AttemptService
from app.utils.similarity import similarity


def test_create_wav_file(mocker: MockerFixture, uow: UnitOfWork) -> None:
    audio_bytes = b"test"

    mock_file = mocker.mock_open()
    mocker.patch("builtins.open", mock_file)

    filename = AttemptService(uow).create_wav_file(audio_bytes)

    mock_file.assert_called_once_with(filename, "bx")
    mock_file().write.assert_called_once_with(audio_bytes)


@pytest.mark.parametrize(
    "s1, s2, expected",
    [
        (["a", "b", "c"], ["a", "b", "c"], 100),
        (["a", "b", "c"], ["d", "e", "f"], 0),
        (["a", "b", "c"], ["a", "b", "d"], 67),
        (["a", "b", "c"], ["a", "b", "c", "d"], 75),
        (["a", "b", "c"], ["a", "c", "b", "d"], 50),
        (["a", "b", "c"], ["c", "a", "b"], 33),
    ],
)
def test_similarity(s1: list[str], s2: list[str], expected: int) -> None:
    assert similarity(s1, s2) == expected


def test_post_attempt(session: Session, uow: UnitOfWork, mocker: MockerFixture, auth_client: TestClient) -> None:
    # Check that calls to:
    # create_wav_file, upload_wav_to_s3, dispatch_to_model, similarity are made correctly
    # Recording entry is added to the table
    # File is deleted correctly
    # Correct response is returned
    test_word = "software"
    test_word_phonemes = ["s", "oʊ", "f", "t", "w", "ɛ", "r"]
    similarity = 100

    # mock_os_remove = mocker.patch("os.remove")
    mock_service = mocker.Mock(spec=AttemptService)
    mocker.patch("app.routers.attempts.AttemptService", return_value=mock_service)

    mock_service.post_attempt.return_value = {
        "score": similarity,
        "xp_gain": 1.5 * similarity,
        "recording_id": 1,
        "recording_phonemes": [
            {"ipa": "s", "respelling": "s"},
            {"ipa": "oʊ", "respelling": "oʊ"},
            {"ipa": "f", "respelling": "f"},
            {"ipa": "t", "respelling": "t"},
            {"ipa": "w", "respelling": "w"},
            {"ipa": "ɛ", "respelling": "ɛ"},
            {"ipa": "r", "respelling": "r"},
        ],
    }

    word = uow.words.upsert(Word(text=test_word))
    phonemes = uow.phonemes.upsert_all([Phoneme(ipa=p, respelling=p) for p in test_word_phonemes])
    session.add_all([WordPhonemeLink(word_id=word.id, phoneme_id=p.id, index=i) for i, p in enumerate(phonemes)])
    session.commit()
    unit = uow.units.upsert(Unit(name="test", description="test", order=1))
    lesson = uow.lessons.upsert(Lesson(title="test", unit_id=unit.id, order=1))
    exercise = uow.exercises.upsert(Exercise(lesson_id=lesson.id, word_id=word.id, index=0))
    uow.commit()

    wav_file_path = f"tests/assets/{test_word}.wav"

    with open(wav_file_path, "rb") as f:
        files = {"audio_file": f}

        recording_response = auth_client.post(f"/api/v1/exercises/{exercise.id}/attempts", files=files)
    assert recording_response.status_code == 200
    data = recording_response.json()
    print(f"\nThe data is: {data}")
    assert data["score"] == 100
    assert data["xp_gain"] == 1.5 * 100
    assert data["recording_id"] == 1

    mock_service.post_attempt.assert_called_once()
