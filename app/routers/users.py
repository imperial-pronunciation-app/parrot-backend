from fastapi import APIRouter, Depends
from fastapi_users import schemas

from app.models.user import User
from app.schemas.user import UserCreate, UserDetails, UserUpdate
from app.users import current_active_user, fastapi_users


router = APIRouter()

router.include_router(
    fastapi_users.get_register_router(schemas.BaseUser[int], UserCreate), prefix="/users", tags=["users"]
)
router.include_router(
    fastapi_users.get_users_router(schemas.BaseUser[int], UserUpdate), prefix="/users", tags=["users"]
)


@router.get("/api/v1/user_details", response_model=UserDetails)
async def get_user_details(user: User = Depends(current_active_user)) -> UserDetails:
    return UserDetails(
        id=user.id,
        login_streak=user.login_streak,
        xp_total=user.xp_total,
        email=user.email,
        display_name=user.display_name,
        language=user.language,
        league=user.leaderboard_entry.league,
        avatar=user.avatar,
    )
