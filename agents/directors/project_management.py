"""Director of Project Management & Cross-Functional Operations — the Taylor Desk.

Namesake: Frederick Winslow Taylor, who gave HBS's first operations /
"scientific management" course in 1909.

Updated 2026-09-03: monday.com is real and connected — verified via a
real get_user_context call (Pro tier, currently on an active trial —
confirm the post-trial plan before treating it as permanent). It replaces
Airtable as this Director's actual board/task/timeline tool: Airtable has
never actually shown connected in this chat despite being declared in
config.yaml (checked directly via ListConnectors).
"""
from agents.base_director import BaseDirector, DirectorOutput
from pipelines.pipeline_tracker import PipelineTracker


class ProjectManagementDirector(BaseDirector):
    director_id = "project_management"
    namesake = "Taylor"
    title = "Director of Project Management & Cross-Functional Operations — the Taylor Desk"
    model_ref = "anthropic_pro.fast"

    keywords = [
        "timeline", "deadline", "task", "assign", "owner", "milestone",
        "status", "pipeline", "operations", "sync", "tracking", "plan",
        "sop", "standard operating procedure", "virtual program",
        "in-person event", "scaling", "special project", "monday.com",
        "monday", "board",
    ]

    system_prompt = (
        "You are the Director of Project Management & Cross-Functional "
        "Operations at the HBS AI Institute. You manage timelines, "
        "automatically route tasks to the right owner, maintain separation "
        "of duties across the other Directors' workstreams, and keep "
        "monday.com and Notion as the operational system of record. "
        "monday.com is real and connected as of 2026-09-03 (verified via a "
        "real get_user_context call; currently on a Pro trial — confirm "
        "the post-trial plan before treating it as permanent) — use "
        "mcp__monday_com__* for real, not Airtable, which has never "
        "actually shown connected here despite being declared in "
        "config.yaml. You also develop and document standard operating "
        "procedures for AI-enabled digital learning production and "
        "delivery, manage complex virtual programming, support in-person "
        "event logistics, and own special projects tied to scaling the "
        "Institute. Output a clear task breakdown with owner, dependency, "
        "and target date for every initiative you touch."
    )

    def __init__(self, router=None, tracker: PipelineTracker | None = None):
        super().__init__(router)
        self.tracker = tracker or PipelineTracker()

    def handle(self, task: str, context: str = "") -> DirectorOutput:
        output = super().handle(task, context)
        # Every PM Director pass logs (or updates) a pipeline row so nothing
        # discussed with the Chief of Staff falls out of the tracker.
        sync_result = self.tracker.add_initiative(
            initiative=self._summarize(task, limit=100),
            director="project_management",
            notes=output.summary,
        )
        output.metadata["airtable_sync"] = sync_result
        return output
