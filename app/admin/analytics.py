from sqladmin import ModelView

from app.models.analytics import EndpointAnalytics


class EndpointAnalyticsAdmin(ModelView, model=EndpointAnalytics):  # type: ignore[call-arg]
    column_list = [
        EndpointAnalytics.endpoint,
        EndpointAnalytics.method,
        EndpointAnalytics.status_code,
        EndpointAnalytics.duration,
        EndpointAnalytics.timestamp,
    ]
    name = "Endpoint Analytics"
    name_plural = "Endpoint Analytics"
    can_create = False
    can_edit = False
