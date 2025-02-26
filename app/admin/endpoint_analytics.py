from fastapi import Request
from fastapi.responses import HTMLResponse
from sqladmin import BaseView, expose

from app.services.analytics import AnalyticsService


class AnalyticsDashboard(BaseView):
    name = "API Analytics"
    icon = "fa fa-chart-bar"

    @expose("/analytics", methods=["GET"])
    async def analytics(self, request: Request) -> HTMLResponse:
        chart_data: dict = AnalyticsService().get_chart_data()
        return await self.templates.TemplateResponse(
            request, "admin/analytics.jinja2", context={"chart_data": chart_data}
        )
