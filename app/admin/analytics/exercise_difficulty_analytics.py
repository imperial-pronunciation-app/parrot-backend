from fastapi import Request
from fastapi.responses import HTMLResponse
from sqladmin import BaseView, expose

from app.services.analytics.analytics import AnalyticsService


class ExerciseDifficultyDashboard(BaseView):
    name = "Exercise Difficulty Analytics"
    icon = "fa fa-chart-line"

    @expose("/exercise-difficulty-analytics", methods=["GET"])
    async def exercise_difficulty_analytics(self, request: Request) -> HTMLResponse:
        difficulty_data: dict = AnalyticsService().get_exercise_difficulty_data()
        return await self.templates.TemplateResponse(
            request,
            "admin/analytics.jinja2",
            context={
                "chart_data": difficulty_data,
                "chart_title": "Exercise Difficulty Analysis",
                "chart_x_label": "Exercise IDs",
                "chart_y_label": "Average Score",
            },
        )
