from typing import Protocol

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.models.user import User
from tests.factories.language import LanguageFactory
from tests.utils import register_user


DEFAULT_DISPLAY_NAME = "Test User"
DEFAULT_EMAIL = "test@example.com"
DEFAULT_PASSWORD = "1234"

class UserFactory(Protocol):
    def __call__(self, display_name: str = DEFAULT_DISPLAY_NAME, email: str = DEFAULT_EMAIL, password: str = DEFAULT_PASSWORD, create_language: bool = True) -> User:
        ...

@pytest.fixture
def make_user(session: Session, client: TestClient, make_language: LanguageFactory) -> UserFactory:
    def make(display_name: str = DEFAULT_DISPLAY_NAME, email: str = DEFAULT_EMAIL, password: str = DEFAULT_PASSWORD, create_language: bool = True) -> User:
        if create_language:
            make_language()
        register_user(client, email, display_name, password)
        return session.exec(select(User).where(User.email == email)).one()
    return make