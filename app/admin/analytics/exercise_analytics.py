from fastapi import Request
from fastapi.responses import HTMLResponse
from sqladmin import BaseView, expose

from app.services.analytics.analytics import AnalyticsService


class ExerciseAnalyticsDashboard(BaseView):
    name = "Exercise Analytics"
    icon = "fa fa-chart-bar"

    @expose("/exercise-analytics", methods=["GET"])
    async def exercise_analytics(self, request: Request) -> HTMLResponse:
        exercise_data: dict = AnalyticsService().get_exercise_analytics()
        return await self.templates.TemplateResponse(
            request,
            "admin/analytics.jinja2",
            context={"chart_data": exercise_data, "chart_title": "Exercise Analytics", "chart_x_label": "Exercises", "chart_y_label": "Number of Calls"},
        )
