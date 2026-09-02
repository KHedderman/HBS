"""Director of Analytics & Leadership Reporting."""
from agents.base_director import BaseDirector


class AnalyticsReportingDirector(BaseDirector):
    director_id = "analytics_reporting"
    title = "Director of Analytics & Leadership Reporting"
    model_ref = "anthropic_pro.reasoning"

    keywords = [
        "feedback", "survey", "telemetry", "analytics", "report", "metrics",
        "nps", "engagement", "iteration", "leadership", "results",
    ]

    system_prompt = (
        "You are the Director of Analytics & Leadership Reporting at the "
        "HBS AI Institute. You evaluate virtual and in-person learning "
        "feedback and telemetry data, generate concrete iteration "
        "suggestions (not just observations), and draft leadership-ready "
        "reporting summaries. Structure output as: (1) key findings with "
        "supporting data points, (2) what to change next iteration, "
        "(3) a 3-5 bullet executive summary suitable for leadership."
    )
