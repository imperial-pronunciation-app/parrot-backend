import math

from fastapi.testclient import TestClient

from app.crud.unit_of_work import UnitOfWork
from app.models.leaderboard_user_link import League
from app.models.user import User
from app.services.leaderboard import LeaderboardService
from app.services.user import UserService
from tests.factories.leaderboard_user import DEFAULT_USER_DETAILS as user_details
from tests.factories.leaderboard_user import LeaderboardUsersFactory


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
    assert json["leaders"] == json["user_position"] == [{"id": test_user.id, "rank": 1, "display_name": test_user.display_name, "xp": expected_xp, "avatar": test_user.avatar}]


def test_get_leaderboard(test_user: User, auth_client: TestClient, make_leaderboard_users: LeaderboardUsersFactory) -> None:
    # Setup
    leaderboard_users = make_leaderboard_users(create_language=False)

    # When
    response = auth_client.get("/api/v1/leaderboard/global")
    # Then
    assert response.status_code == 200
    json = response.json()
    assert json["league"] == League.BRONZE

    email_to_id = {link.user.email: link.user_id for link in leaderboard_users}

    assert json["leaders"] == [
        {"id": email_to_id[user_details[0]["email"]], "rank": 1, "display_name": user_details[0]["display_name"], "xp": user_details[0]["xp"], "avatar": leaderboard_users[0].user.avatar},
        {"id": email_to_id[user_details[1]["email"]], "rank": 2, "display_name": user_details[1]["display_name"], "xp": user_details[1]["xp"], "avatar": leaderboard_users[1].user.avatar},
        {"id": email_to_id[user_details[2]["email"]], "rank": 3, "display_name": user_details[2]["display_name"], "xp": user_details[2]["xp"], "avatar": leaderboard_users[2].user.avatar},
    ]
    assert json["user_position"] == [
        {"id": email_to_id[user_details[3]["email"]], "rank": 4, "display_name": user_details[3]["display_name"], "xp": user_details[3]["xp"], "avatar": leaderboard_users[3].user.avatar},
        {"id": email_to_id[user_details[4]["email"]], "rank": 5, "display_name": user_details[4]["display_name"], "xp": user_details[4]["xp"], "avatar": leaderboard_users[4].user.avatar},
        {"id": test_user.id, "rank": 6, "display_name": test_user.display_name, "xp": 0, "avatar": test_user.avatar},
    ]


def test_promotion_demotion(uow: UnitOfWork, make_leaderboard_users: LeaderboardUsersFactory) -> None:    
    # Pre: ensure the sample leaderboard users are in the correct order
    silver_leaderboard_users = make_leaderboard_users(league=League.SILVER)
    assert all(silver_leaderboard_users[i].xp >= silver_leaderboard_users[i + 1].xp for i in range(len(silver_leaderboard_users) - 1))
    
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
    assert silver_leaderboard_users[0].id == gold[0].id
    assert silver_leaderboard_users[1].id == silver[0].id
    assert silver_leaderboard_users[2].id == silver[1].id
    assert silver_leaderboard_users[3].id == silver[2].id
    assert silver_leaderboard_users[4].id == bronze[0].id
