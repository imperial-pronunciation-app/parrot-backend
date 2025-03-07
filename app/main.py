import os

import rollbar
from fastapi import FastAPI
from rollbar.contrib.fastapi import add_to as rollbar_add_to
from sqladmin import Admin

from app.admin import views
from app.admin.auth import AdminAuth
from app.config import get_settings
from app.database import engine
from app.middleware.analytics import AnalyticsMiddleware
from app.middleware.rollbar import setup_exception_handlers
from app.routers import routers


rollbar.init(
    get_settings().ROLLBAR_ACCESS_TOKEN,
    environment=get_settings().ROLLBAR_ENVIRONMENT,
    handler="async",
    include_request_body=True,
)

app = FastAPI()
app.add_middleware(AnalyticsMiddleware)
rollbar_add_to(app)

setup_exception_handlers(app)

base_dir = os.path.join(os.path.dirname(__file__), "..")
templates_dir = os.path.join(base_dir, "app", "admin", "templates")
admin = Admin(app, engine, authentication_backend=AdminAuth(), templates_dir=templates_dir)


for view in views:
    admin.add_view(view)


for router in routers:
    app.include_router(router)


if __name__ == "__main__":
    pass
