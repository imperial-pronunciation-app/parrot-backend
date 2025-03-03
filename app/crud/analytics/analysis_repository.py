from typing import Any, Sequence, Tuple

from sqlmodel import Session, col, func, select

from app.database import engine
from app.models.analytics.analytics import EndpointAnalytics
from app.models.attempt import Attempt
from app.models.exercise import Exercise
from app.models.exercise_attempt import ExerciseAttempt


class AnalyticsRepository:
    def get_count_of_endpoint_and_response_time(self) -> Sequence[Tuple[str, int, Any]]:
        with Session(engine) as session:
            stmt = select(
                EndpointAnalytics.endpoint,
                func.count(col(EndpointAnalytics.endpoint)).label("count"),
                func.avg(EndpointAnalytics.duration).label("avg_response_time"),
            ).group_by(EndpointAnalytics.endpoint)

            results: Sequence[Tuple[str, int, Any]] = session.exec(stmt).fetchall()
            return results

    def upsert_analytics(self, analytics: EndpointAnalytics) -> None:
        with Session(engine) as session:
            session.add(analytics)
            session.commit()

    def get_exercise_analytics(self) -> Sequence[Tuple[str, int]]:
        with Session(engine) as session:
            stmt = (
                select(
                    EndpointAnalytics.endpoint,
                    func.count(col(EndpointAnalytics.endpoint)).label("count"),
                )
                .where(col(EndpointAnalytics.endpoint).contains("exercise"))
                .where(~col(EndpointAnalytics.endpoint).contains("admin"))
                .group_by(EndpointAnalytics.endpoint)
                .order_by("count")  # type: ignore[arg-type]
            )

            result = session.exec(stmt).fetchall()
            return result

    def get_exercise_difficulty_analytics(self) -> Sequence[Tuple[int, float, int]]:
        with Session(engine) as session:
            stmt = (
                select(
                    Exercise.id,
                    func.avg(Attempt.score).label("average_score"),
                    func.count(col(Attempt.id)).label("attempt_count"),
                )
                .join(ExerciseAttempt, ExerciseAttempt.exercise_id == Exercise.id)  # type: ignore[arg-type]
                .join(Attempt, Attempt.id == ExerciseAttempt.id)  # type: ignore[arg-type]
                .group_by(col(Exercise.id))
                .order_by("average_score")  # Order by difficulty (lower scores first)
            )

            return session.exec(stmt).fetchall()
