import math
from typing import List, Sequence

from fastapi.testclient import TestClient

from app.crud.unit_of_work import UnitOfWork
from app.models.leaderboard_user_link import LeaderboardUserLink, League
from app.models.user import User
from app.services.leaderboard import LeaderboardService
from app.services.user import UserService
from tests.fixtures.leaderboard_data import TEST_EMAILS, TEST_XPS


def test_update_xp_existing_record(test_user: User, uow: UnitOfWork) -> None:
    # Pre
    user_service = UserService(uow)
    xp_gain = 50
    prev_league = test_user.leaderboard_entry.league
    prev_xp = test_user.leaderboard_entry.xp

    # When
    leaderboard_user = user_service.update_xp(test_user, xp_gain)

    # Then
    assert leaderboard_user.user_id == test_user.id
    assert leaderboard_user.league == prev_league
    assert leaderboard_user.xp == prev_xp + xp_gain


def test_reset_leaderboard(test_user: User, auth_client: TestClient, uow: UnitOfWork) -> None:
    # Pre
    initial_xp = 10
    user_service = UserService(uow)
    user_service.update_xp(test_user, initial_xp)
    assert test_user.leaderboard_entry.xp == initial_xp

    # When
    leaderboard_service = LeaderboardService(uow)
    leaderboard_service.reset_leaderboard()
    response = auth_client.get("/api/v1/leaderboard/global")

    # Then
    expected_xp = int(math.log2(initial_xp + 1))
    assert uow.leaderboard_users.get_by_user(test_user.id).xp == expected_xp
    assert response.status_code == 200
    json = response.json()
    assert json["league"] == League.SILVER # Promotion
    assert json["leaders"] == json["user_position"] == [{"id": test_user.id, "rank": 1, "username": test_user.email, "xp": expected_xp}]


def test_get_leaderboard(test_user: User, auth_client: TestClient, sample_leaderboard_users_bronze: List[LeaderboardUserLink]) -> None:
    # When
    response = auth_client.get("/api/v1/leaderboard/global")
    # Then
    assert response.status_code == 200
    json = response.json()
    assert json["league"] == League.BRONZE

    email_to_id = {link.user.email: link.user_id for link in sample_leaderboard_users_bronze}

    assert json["leaders"] == [
        {"id": email_to_id[TEST_EMAILS[0]], "rank": 1, "username": TEST_EMAILS[0], "xp": TEST_XPS[0]},
        {"id": email_to_id[TEST_EMAILS[1]], "rank": 2, "username": TEST_EMAILS[1], "xp": TEST_XPS[1]},
        {"id": email_to_id[TEST_EMAILS[2]], "rank": 3, "username": TEST_EMAILS[2], "xp": TEST_XPS[2]},
    ]
    assert json["user_position"] == [
        {"id": email_to_id[TEST_EMAILS[3]], "rank": 4, "username": TEST_EMAILS[3], "xp": TEST_XPS[3]},
        {"id": email_to_id[TEST_EMAILS[4]], "rank": 5, "username": TEST_EMAILS[4], "xp": TEST_XPS[4]},
        {"id": test_user.id, "rank": 6, "username": test_user.email, "xp": 0},
    ]


def test_promotion_demotion(uow: UnitOfWork, sample_leaderboard_users_silver: Sequence[LeaderboardUserLink]) -> None:    
    # Pre: ensure the sample leaderboard users are in the correct order
    assert all(sample_leaderboard_users_silver[i].xp >= sample_leaderboard_users_silver[i + 1].xp for i in range(len(sample_leaderboard_users_silver) - 1))
    
    # When
    leaderboard_service = LeaderboardService(uow)
    leaderboard_service.reset_leaderboard()

    # Then
    leaderboard_users = uow.leaderboard_users.all()
    gold = [user for user in leaderboard_users if user.league == League.GOLD]
    silver = sorted([user for user in leaderboard_users if user.league == League.SILVER], key=lambda x: x.xp, reverse=True)
    bronze = [user for user in leaderboard_users if user.league == League.BRONZE]

    assert len(gold) == 1
    assert len(silver) == 3
    assert len(bronze) == 1
    assert gold[0].xp >= silver[0].xp
    assert bronze[0].xp <= silver[2].xp
    assert sample_leaderboard_users_silver[0].id == gold[0].id
    assert sample_leaderboard_users_silver[1].id == silver[0].id
    assert sample_leaderboard_users_silver[2].id == silver[1].id
    assert sample_leaderboard_users_silver[3].id == silver[2].id
    assert sample_leaderboard_users_silver[4].id == bronze[0].id
