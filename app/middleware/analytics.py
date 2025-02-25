from datetime import datetime

from fastapi import FastAPI, Request
from sqlmodel import Session
from starlette.types import Receive, Scope, Send

from app.database import engine
from app.models.analytics import EndpointAnalytics


class AnalyticsMiddleware:
    def __init__(self, app: FastAPI) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        start_time = datetime.now()

        # Create a new Request instance
        request = Request(scope, receive)

        # Create a response tracker
        response_info = {"status_code": 0}

        async def send_wrapper(message: dict) -> None:
            if message["type"] == "http.response.start":
                response_info["status_code"] = message["status"]
            await send(message)

        # Process the request
        await self.app(scope, receive, send_wrapper)

        # Calculate duration
        duration = (datetime.now() - start_time).total_seconds()

        # Record analytics
        analytics = EndpointAnalytics(
            endpoint=request.url.path,
            method=request.method,
            status_code=response_info["status_code"],
            duration=duration,
            timestamp=start_time,
        )

        # Save to database
        with Session(engine) as session:
            session.add(analytics)
            session.commit()
