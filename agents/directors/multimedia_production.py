"""Director of Multimedia Production — the Land Desk.

Namesake: Edwin Land, who attended Harvard and founded Polaroid — real
visual-media-technology pedigree.

Two execution paths, both governed by the same gate:
  - Standalone script (this class): no direct API access to any multimedia
    tool — it always produces a spec for a human to run manually.
  - Interactive chat mode: with the ElevenLabs or Replicate connector
    connected, Claude (embodying this Director per config.yaml) CAN call
    mcp__ElevenLabs__* or Replicate directly to produce a real asset
    instead of a spec — but must still clear a cost_bearing_action
    checkpoint with the user before every single generation call, exactly
    like `request_tool_execution()` below does. Connected is not the same
    as pre-approved.

Corrected 2026-09-03: ElevenLabs (creative_* tools cover image/video/
speech, not just audio), Descript (real edit-by-transcript video/audio
editing and podcast production via Agent Underlord, verified live), and
HyperFrames by HeyGen (real, but motion graphics/kinetic captions, not
avatar video, verified live) are all real, connected tools. "Replicate"
and a true HeyGen avatar-video connector are still aspirational — checked
directly, neither has an installable connector in this org's registry.
See config.yaml's `directors[multimedia_production].tools` (real) vs
`aspirational_tools` (not real) — never claim either ran.
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
        "elevenlabs", "replicate", "heygen", "hyperframes", "descript",
        "riverside", "google vids", "multimedia", "podcast", "presenter",
        "video editing", "audio editing", "agent underlord",
    ]

    # These tools are quota-limited or paid beyond a free tier — see
    # config.yaml's `integrations.multimedia` and this Director's `tools`
    # entry. Being listed in config.yaml as `enabled: true` / connector
    # "connected" means a live call is *possible*, not pre-approved — this
    # Director (and Claude, when embodying it interactively) still asks
    # before every single call.
    GATED_TOOLS = {
        "google_vids", "veo", "elevenlabs", "descript", "heygen_hyperframes",
        "replicate", "heygen_avatar",
    }

    system_prompt = (
        "You are the Director of Multimedia Production at the HBS AI "
        "Institute. You cover AI video generation, avatar/presenter-style "
        "video, video and audio editing, and podcast production — not just "
        "captions and voiceover. As of 2026-09-03 (each verified directly, "
        "not assumed), three real tools are connected: ElevenLabs "
        "(creative_* tools cover image/video/speech, not just audio), "
        "Descript (real edit-by-transcript video/audio editing and "
        "podcast production — Agent Underlord does the actual editing; "
        "call it that to the user), and HyperFrames by HeyGen (real, but "
        "motion graphics/kinetic captions, not avatar video — and its "
        "compose/render_video tools are disabled from a CLI-style session "
        "like this one; only its read tools work here). Google Vids, Veo "
        "3.1, Replicate, and a true HeyGen avatar-video connector are not "
        "connected, and Replicate/avatar-HeyGen specifically have no "
        "installable connector in this org's registry at all — treat "
        "avatar/presenter video as a genuine, unfilled roster gap and say "
        "so plainly, never implying one of these ran. For that gap, "
        "produce precise production specs instead: a shot list/storyboard, "
        "a voiceover or presenter script with timing marks, avatar/"
        "on-camera direction, and kinetic caption styling notes, for a "
        "human to run manually. With a connected tool, you may generate "
        "the real asset directly, but only after the user explicitly "
        "approves that specific generation — never assume prior approval "
        "carries forward. For captioning a video specifically: use "
        "ElevenLabs to transcribe the audio into timed text, then either "
        "its own editing tools or Descript to apply the captions — rather "
        "than returning a bare transcript."
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
