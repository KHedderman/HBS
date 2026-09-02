"""Director of Multimedia Production."""
from agents.base_director import BaseDirector, DirectorOutput
from agents.llm_provider import PaidTierRequiredError


class MultimediaProductionDirector(BaseDirector):
    director_id = "multimedia_production"
    title = "Director of Multimedia Production"
    model_ref = "anthropic_pro.chat"  # used for orchestration/scripting only

    keywords = [
        "video", "audio", "avatar", "caption", "voiceover", "veo",
        "elevenlabs", "descript", "google vids", "multimedia",
    ]

    # These tools are quota-limited or paid beyond a free tier — see
    # config.yaml's `integrations.multimedia`. This Director orchestrates
    # scripts/specs for them but never assumes it can call them directly.
    GATED_TOOLS = {"google_vids", "veo", "elevenlabs", "descript"}

    system_prompt = (
        "You are the Director of Multimedia Production at the HBS AI "
        "Institute. You orchestrate Google Vids, Veo 3.1, ElevenLabs, and "
        "Descript by producing precise production specs: a shot list / "
        "storyboard, a voiceover script with timing marks, avatar/on-camera "
        "direction, and kinetic caption styling notes. You do not have "
        "direct API access to these tools by default (they are quota- or "
        "cost-gated) — produce the spec a human will feed into each tool "
        "manually, unless told the integration is live."
    )

    def request_tool_execution(self, tool: str, hitl_gate) -> str:
        """Any attempt to actually invoke a gated multimedia tool (as
        opposed to producing a spec for a human to run manually) must clear
        the cost governance checkpoint first.
        """
        if tool not in self.GATED_TOOLS:
            return "keep_free_path"
        try:
            raise PaidTierRequiredError(
                tool, "Multimedia tool is quota-limited/paid beyond the free tier."
            )
        except PaidTierRequiredError as exc:
            return hitl_gate.present_cost_choice(tool, str(exc))

    def handle(self, task: str, context: str = "") -> DirectorOutput:
        output = super().handle(task, context)
        output.metadata["gated_tools"] = sorted(self.GATED_TOOLS)
        return output
