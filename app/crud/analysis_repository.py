from typing import Any, Sequence, Tuple

from sqlmodel import Session, func, select

from app.database import engine
from app.models.analytics import EndpointAnalytics


class AnalyticsRepository:
    def get_count_of_endpoint_and_response_time(self) -> Sequence[Tuple[str, int, Any]]:
        with Session(engine) as session:
            stmt = select(
                EndpointAnalytics.endpoint,
                func.count().label("count"),
                func.avg(EndpointAnalytics.duration).label("avg_response_time"),
            ).group_by(EndpointAnalytics.endpoint)

            results: Sequence[Tuple[str, int, Any]] = session.exec(stmt).fetchall()
            return results

    def upsert_analytics(self, analytics: EndpointAnalytics) -> None:
        with Session(engine) as session:
            session.add(analytics)
            session.commit()
