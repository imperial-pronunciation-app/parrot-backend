from datetime import date, timedelta
from typing import Optional

import pytest
from fastapi.testclient import TestClient

from app.crud.unit_of_work import UnitOfWork
from app.models.user import Avatar, User
from app.services.user import UserService
from tests.factories.language import LanguageFactory
from tests.utils import register_user


UPDATE_ENDPOINT = "/users/me"

def test_register_user(client: TestClient, make_language: LanguageFactory) -> None:
    """Should successfully register a user."""
    make_language()
    response = register_user(client)

    assert response.status_code == 201, f"Unexpected status: {response.status_code}, response: {response.json()}"

@pytest.mark.parametrize(
    "email, display_name, password, expected_status",
    [
        ("newuser@example.com", "New User", None, 422), # Missing password
        ("newuser@example.com", None, "password", 422), # Missing display name
        (None, "New User", "password", 422),            # Missing email
        (None, None, None, 422),                        # Missing all
    ]
)
def test_register_user_invalid_cases(client: TestClient, email: Optional[str], display_name: Optional[str], password: Optional[str], expected_status: int) -> None:
    """Should return correct status codes for invalid login attempts."""
    response = register_user(client, email=email, display_name=display_name, password=password)

    assert response.status_code == expected_status, f"Unexpected status: {response.status_code}, response: {response.json()}"

def test_update_user(auth_client: TestClient, make_language: LanguageFactory, uow: UnitOfWork) -> None:
    """Should successfully update a user's email, language and avatar."""

    # Pre
    language = make_language(is_default=False)
    email = "newemail@example.com"

    # When
    response = auth_client.patch(
        UPDATE_ENDPOINT,
        json={
            "email": email,
            "language_id": language.id,
            "avatar": Avatar.BROWN,
        }
    )

    # Then
    assert response.status_code == 200
    user = uow.users.get_by_email(email)
    assert user.email == email
    assert user.language_id == language.id
    assert user.avatar == Avatar.BROWN

def test_update_user_existing_email(client: TestClient, auth_client: TestClient) -> None:
    """Should return 401 when attempting to update user without a token."""
    email = "otheruser@example.com"
    register_user(client, email)

    response = auth_client.patch(
        UPDATE_ENDPOINT,
        json={"email": email}
    )
    assert response.status_code == 400

def test_update_login_streak(test_user: User, uow: UnitOfWork) -> None:
    """Should increment the user's login streak."""

    # Pre
    old_login_streak = 1
    test_user.last_login_date = date.today() - timedelta(days=1)
    test_user.login_streak = old_login_streak
    test_user = uow.users.upsert(test_user)
    uow.commit()

    # When
    user_service = UserService(uow)
    updated_user = user_service.update_login_streak(test_user)

    # Then
    assert updated_user.login_streak == old_login_streak + 1

def test_break_login_streak(test_user: User, uow: UnitOfWork) -> None:
    """Should reset the user's login streak to 1."""

    # Pre
    test_user.last_login_date = date.today() - timedelta(days=2)
    test_user.login_streak = 5
    test_user = uow.users.upsert(test_user)
    uow.commit()

    # When
    user_service = UserService(uow)
    updated_user = user_service.update_login_streak(test_user)

    # Then
    assert updated_user.login_streak == 1

def test_unchanged_login_streak(test_user: User, uow: UnitOfWork) -> None:
    """Should keep the user's login streak unchanged."""

    # Pre
    old_login_streak = 5
    test_user.last_login_date = date.today()
    test_user.login_streak = old_login_streak
    test_user = uow.users.upsert(test_user)
    uow.commit()

    # When
    user_service = UserService(uow)
    updated_user = user_service.update_login_streak(test_user)

    # Then
    assert updated_user.login_streak == old_login_streak

def test_get_user_details(auth_client: TestClient, test_user: User) -> None:
    """Should return the user's details."""

    # When
    response = auth_client.get("/api/v1/user_details")

    # Then
    assert response.status_code == 200
    json = response.json()
    assert json["id"] == test_user.id
    assert json["login_streak"] == test_user.login_streak
    assert json["xp_total"] == test_user.xp_total
    assert json["email"] == test_user.email
    assert json["display_name"] == test_user.display_name
    assert json["language"] == test_user.language.model_dump()
    assert json["league"] == test_user.leaderboard_entry.league

def test_users_me_does_not_expose_password_hash(auth_client: TestClient) -> None:
    """Should not expose the user's password hash."""

    # When
    response = auth_client.get("/users/me")

    # Then
    assert response.status_code == 200
    json = response.json()
    assert "password" not in json
    assert "hashed_password" not in json
