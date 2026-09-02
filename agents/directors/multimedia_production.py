"""Director of Multimedia Production — the Land Desk.

Namesake: Edwin Land, who attended Harvard and founded Polaroid — real
visual-media-technology pedigree.

Two execution paths, both governed by the same gate:
  - Standalone script (this class): no direct API access to any multimedia
    tool — it always produces a spec for a human to run manually.
  - Interactive chat mode: with the ElevenLabs connector connected, Claude
    (embodying this Director per config.yaml) CAN call mcp__ElevenLabs__*
    directly to produce a real asset instead of a spec — but must still
    clear a cost_bearing_action checkpoint with the user before every
    single generation call, exactly like `request_tool_execution()` below
    does. Connected is not the same as pre-approved.
"""
from agents.base_director import BaseDirector, DirectorOutput
from agents.llm_provider import PaidTierRequiredError


class MultimediaProductionDirector(BaseDirector):
    director_id = "multimedia_production"
    namesake = "Land"
    title = "Director of Multimedia Production — the Land Desk"
    model_ref = "anthropic_pro.chat"  # used for orchestration/scripting only

    keywords = [
        "video", "audio", "avatar", "caption", "voiceover", "veo",
        "elevenlabs", "descript", "google vids", "multimedia",
    ]

    # These tools are quota-limited or paid beyond a free tier — see
    # config.yaml's `integrations.multimedia`. Being listed in config.yaml
    # as `enabled: true` / connector "connected" means a live call is
    # *possible*, not pre-approved — this Director (and Claude, when
    # embodying it interactively) still asks before every single call.
    GATED_TOOLS = {"google_vids", "veo", "elevenlabs", "descript"}

    system_prompt = (
        "You are the Director of Multimedia Production at the HBS AI "
        "Institute. You orchestrate Google Vids, Veo 3.1, ElevenLabs, and "
        "Descript by producing precise production specs: a shot list / "
        "storyboard, a voiceover script with timing marks, avatar/on-camera "
        "direction, and kinetic caption styling notes. In the standalone "
        "script you never call these tools directly — you produce the spec "
        "a human runs manually. In an interactive chat session with a "
        "connector connected (e.g. ElevenLabs), you may generate the real "
        "asset directly, but only after the user explicitly approves that "
        "specific generation — never assume prior approval carries forward."
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
