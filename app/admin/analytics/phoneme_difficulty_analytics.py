from fastapi import Request
from fastapi.responses import HTMLResponse
from sqladmin import BaseView, expose

from app.services.analytics.analytics import AnalyticsService


class PhonemeDifficultyDashboard(BaseView):
    name = "Phoneme Difficulty Analytics"
    icon = "fa fa-chart-line"

    @expose("/phoneme-difficulty-analytics", methods=["GET"])
    async def phoneme_difficulty_analytics(self, request: Request) -> HTMLResponse:
        difficulty_data: dict = AnalyticsService().get_phoneme_difficulty_data()
        return await self.templates.TemplateResponse(
            request,
            "admin/analytics.jinja2",
            context={
                "chart_data": difficulty_data,
                "chart_title": "Phoneme Difficulty Analysis",
                "chart_x_label": "Phonemes",
                "chart_y_label": "Average Score",
            },
        )
