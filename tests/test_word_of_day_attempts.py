# import pytest
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture

from app.models.user import User
from app.services.attempts import AttemptService
from tests.factories.word_of_day import WordOfDayFactory


def test_word_of_day_attempts(
    mocker: MockerFixture, auth_client: TestClient, make_word_of_day: WordOfDayFactory, test_user: User
) -> None:
    """Test post_word_of_day_attempt"""
    language = test_user.language

    word_of_day = make_word_of_day(text="software", language=language)
    test_word = word_of_day.word
    similarity = 100
    xp_gain = 1.5 * similarity
    recording_id = 1

    # mock_os_remove = mocker.patch("os.remove")
    mock_service = mocker.Mock(spec=AttemptService)
    mocker.patch("app.routers.attempts.AttemptService", return_value=mock_service)
    mock_service.post_word_of_day_attempt.return_value = {
        "success": True,
        "score": similarity,
        "xp_gain": xp_gain,
        "recording_id": recording_id,
        "phonemes": [],
    }

    wav_file_path = f"tests/assets/{test_word.text}.wav"
    with open(wav_file_path, "rb") as f:
        files = {"audio_file": f}

        recording_response = auth_client.post("/api/v1/word_of_day/attempts", files=files)
    assert recording_response.status_code == 200
    data = recording_response.json()
    assert data["score"] == similarity
    assert data["xp_gain"] == xp_gain
    assert data["recording_id"] == recording_id

    mock_service.post_word_of_day_attempt.assert_called_once()
