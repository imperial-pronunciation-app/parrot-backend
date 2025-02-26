from datetime import datetime

from sqlmodel import Field

from app.models.id_model import IdModel


class EndpointAnalytics(IdModel, table=True):
    endpoint: str = Field(default=None)
    method: str = Field(default=None)
    status_code: int = Field(default=None)
    duration: float = Field(default=0)
    timestamp: datetime = Field(default_factory=datetime.now)
    