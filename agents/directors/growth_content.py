"""Director of Growth & Omnichannel Content."""
from agents.base_director import BaseDirector, DirectorOutput


class GrowthContentDirector(BaseDirector):
    director_id = "growth_content"
    title = "Director of Growth & Omnichannel Content"
    model_ref = "anthropic_pro.chat"

    keywords = [
        "linkedin", "newsletter", "instagram", "social", "post", "content",
        "growth", "audience", "recycle", "repurpose", "marketing",
    ]

    system_prompt = (
        "You are the Director of Growth & Omnichannel Content at the HBS AI "
        "Institute. You draft LinkedIn posts, newsletters, and Instagram "
        "posts; provide creative consulting and growth strategy to attract "
        "learners; and act as a 'content recycler' that turns long-form "
        "research or course material into multi-channel assets. Always "
        "produce channel-native variants (not one post copy-pasted three "
        "times) and flag anything making an external claim for the "
        "'external_publish' HITL checkpoint before it's posted."
    )

    def recycle(self, long_form_source: str) -> DirectorOutput:
        """Turns long-form research/course material into a multi-channel
        content set: LinkedIn post, newsletter blurb, Instagram caption.
        """
        task = (
            "Recycle the following long-form source into three assets: "
            "1) a LinkedIn post, 2) a newsletter section, 3) an Instagram "
            "caption + hashtag set. Preserve the core insight in each.\n\n"
            f"SOURCE:\n{long_form_source}"
        )
        return self.handle(task)

    def handle(self, task: str, context: str = "") -> DirectorOutput:
        output = super().handle(task, context)
        if "post" in task.lower() or "publish" in task.lower():
            output.requires_hitl = "external_publish"
        return output
