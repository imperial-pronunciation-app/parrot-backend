import os
from typing import Dict

import rollbar
from fastapi import FastAPI, HTTPException
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


@app.get("/")
def read_home() -> Dict[str, str]:  # would be a Pydantic return type normally
    return {"Hello": "James"}


@app.get("/test-rollbar")
def test_rollbar() -> float:
    return 1 / 0


# Add test endpoints to generate different error types
@app.get("/test/404")
async def test_404() -> None:
    """Test endpoint that returns a 404 error"""
    raise HTTPException(status_code=404, detail="Resource not found")


@app.get("/test/401")
async def test_401() -> None:
    """Test endpoint that returns a 401 error"""
    raise HTTPException(status_code=401, detail="Not authorized")


@app.get("/test/500")
async def test_500() -> None:
    """Test endpoint that returns a 500 error"""
    raise Exception("This is a test 500 error")


for router in routers:
    app.include_router(router)


if __name__ == "__main__":
    pass
