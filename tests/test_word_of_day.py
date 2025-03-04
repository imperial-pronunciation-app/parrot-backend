from fastapi.testclient import TestClient

from app.crud.unit_of_work import UnitOfWork
from app.services.word_of_day import WordOfDayService
from tests.factories.language import LanguageFactory
from tests.factories.word import WordFactory
from tests.factories.word_of_day import WordOfDayFactory


def test_get_word_of_day(auth_client: TestClient, make_word_of_day: WordOfDayFactory) -> None:
    """Test retrieving the word of the day with corresponding phonemes."""

    # When
    word_of_day = make_word_of_day()
    language = word_of_day.word.language
    assert word_of_day.id is not None
    response = auth_client.get(f"/api/v1/{language.name}/word_of_day")

    # Then
    assert response.status_code == 200
    data = response.json()
    assert data["text"] == word_of_day.word.text
    assert data["id"] == word_of_day.word_id
    assert data["phonemes"] is not None

def test_assign_new_word_of_day(uow: UnitOfWork, make_word: WordFactory) -> None:
    """Tests the adding of a new word of the day to the database."""
    word = make_word()

    # When
    WordOfDayService(uow).change_word_of_day()

    # Then
    word_of_day = uow.word_of_day.get_word_of_day(word.language.id)
    assert word_of_day.id is word.id
    assert word_of_day.word_id is word.id


def test_get_new_word_unauthorized(client: TestClient, make_language: LanguageFactory) -> None:
    """Test that unauthorized requests get a 401 error."""
    language = make_language()

    # When
    response = client.get(f"/api/v1/{language.name}/word_of_day")

    # Then
    assert response.status_code == 401
