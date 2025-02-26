from fastapi import Request
from fastapi_users.password import PasswordHelper
from sqladmin.authentication import AuthenticationBackend

from app.config import get_settings


# Define authentication logic
class AdminAuth(AuthenticationBackend):
    def __init__(self) -> None:
        super().__init__(get_settings().USER_MANAGER_SECRET)
        self._admin_username = get_settings().ADMIN_USERNAME
        self._admin_password_hash = get_settings().ADMIN_PASSWORD_HASH
        self._password_helper = PasswordHelper()

    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")
        if (
            username == self._admin_username
            and self._password_helper.verify_and_update(password, f"{self._admin_password_hash.strip('’').strip('‘')}")[
                0
            ]
        ):
            request.session.update({"authenticated": True})
            return True
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        return bool(request.session.get("authenticated", False))
