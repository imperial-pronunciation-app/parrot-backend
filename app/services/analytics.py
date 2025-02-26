from app.crud.analysis_repository import AnalyticsRepository


class AnalyticsService:
    def get_chart_data(self) -> dict:
        
        # Sadly, we can't use the UnitOfWork pattern here, as this service is called from the admin panel
        results = AnalyticsRepository().get_count_of_endpoint_and_response_time()

        endpoints: list[str] = [str(r[0]) for r in results]
        counts: list[int] = [int(r[1]) for r in results]
        avg_times: list[float] = [round(float(r[2]), 2) if r[2] is not None else 0.0 for r in results]

        results_filtered: list[tuple[str, int, float]] = [
            (endpoint, count, avg_time)
            for endpoint, count, avg_time in zip(endpoints, counts, avg_times)
            if "admin" not in endpoint
        ]

        if results_filtered:
            endpoints, counts, avg_times = map(list, zip(*results_filtered))
        else:
            endpoints, counts, avg_times = [], [], []

        chart_data = {
            "labels": endpoints,
            "datasets": [
                {
                    "label": "Number of Calls",
                    "data": counts,
                    "backgroundColor": "rgba(75, 192, 192, 0.5)",
                    "borderColor": "rgb(75, 192, 192)",
                    "borderWidth": 1,
                },
                {
                    "label": "Avg Response Time (ms)",
                    "data": avg_times,
                    "backgroundColor": "rgba(255, 99, 132, 0.5)",
                    "borderColor": "rgb(255, 99, 132)",
                    "borderWidth": 1,
                    "yAxisID": "response-time",
                },
            ],
        }
        return chart_data
