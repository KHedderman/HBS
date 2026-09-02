"""Director of Project Management & Cross-Functional Operations."""
from agents.base_director import BaseDirector, DirectorOutput
from pipelines.pipeline_tracker import PipelineTracker


class ProjectManagementDirector(BaseDirector):
    director_id = "project_management"
    title = "Director of Project Management & Cross-Functional Operations"
    model_ref = "anthropic_pro.fast"

    keywords = [
        "timeline", "deadline", "task", "assign", "owner", "milestone",
        "status", "pipeline", "operations", "sync", "tracking", "plan",
    ]

    system_prompt = (
        "You are the Director of Project Management & Cross-Functional "
        "Operations at the HBS AI Institute. You manage timelines, "
        "automatically route tasks to the right owner, maintain separation "
        "of duties across the other Directors' workstreams, and keep "
        "Airtable and Notion as the operational system of record. Output a "
        "clear task breakdown with owner, dependency, and target date for "
        "every initiative you touch."
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
