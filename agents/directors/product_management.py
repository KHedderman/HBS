"""Director of AI Product Management & Development — the Aiken Desk.

Namesake: Howard Aiken, the Harvard professor who built the Harvard Mark I
— a real builder/engineer pedigree for this Director's PRD/architecture/PR work.
"""
from agents.base_director import BaseDirector, DirectorOutput
from database_sync import github_sync


class ProductManagementDirector(BaseDirector):
    director_id = "product_management"
    namesake = "Aiken"
    title = "Director of AI Product Management & Development — the Aiken Desk"
    model_ref = "anthropic_pro.reasoning"

    keywords = [
        "feature", "prd", "spec", "architecture", "code", "pr", "pull request",
        "repo", "ship", "release", "qa", "bug", "roadmap", "requirements",
    ]

    system_prompt = (
        "You are the Director of AI Product Management & Development at the "
        "HBS AI Institute. You operate as: (1) a feature ideator, (2) a PRD "
        "generator (produce a full PRD with problem statement, users, "
        "requirements, success metrics, and risks), (3) a technical architect "
        "(propose a concrete, minimal architecture), (4) a ship QA reviewer "
        "(list concrete test cases and edge cases), and (5) the direct "
        "code/PR sync manager for GitHub. Any action that would open a PR or "
        "merge code requires the 'external_publish' HITL checkpoint — draft "
        "the change, but do not claim it has shipped."
    )

    def handle(self, task: str, context: str = "") -> DirectorOutput:
        output = super().handle(task, context)
        publish_signals = ("open a pr", "create a pr", "merge", "push to github", "ship it")
        if any(sig in task.lower() for sig in publish_signals):
            output.requires_hitl = "external_publish"
        return output

    def sync_pr_draft(self, relative_path: str, content: str, commit_message: str) -> dict:
        """Called only after the external_publish HITL checkpoint has been
        approved by the Chief of Staff. Writes/commits the artifact via the
        shared GitHub sync adapter.
        """
        return github_sync.push_memory_file(relative_path, content, commit_message)
