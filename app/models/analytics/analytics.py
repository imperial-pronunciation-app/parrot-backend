from datetime import datetime

from sqlmodel import Field

from app.models.analytics.http_method import HTTPMethod
from app.models.id_model import IdModel


class EndpointAnalytics(IdModel, table=True):
    endpoint: str
    method: HTTPMethod
    status_code: int
    duration: float = Field(nullable=False, default=0)
    timestamp: datetime = Field(default_factory=datetime.now, nullable=False)
