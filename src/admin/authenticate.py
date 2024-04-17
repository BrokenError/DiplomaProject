import uuid

from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from settings import settings_app


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]
        if username == settings_app.COMPANY_USERNAME_ADMIN and password == settings_app.COMPANY_PASSWORD_ADMIN:
            request.session.update({"token": f"{uuid.uuid4()}"})
            return True
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False

        return True


authentication_backend = AdminAuth(secret_key=settings_app.SECRET_KEY)
