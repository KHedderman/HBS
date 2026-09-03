"""Director of Content Conversion & Production — the Copeland Desk.

Namesake: Melvin T. Copeland, credited with writing HBS's first
course-method case (1921) — the person who formalized converting raw
research into a usable teaching asset, which is exactly this Director's job.

Added to cover a real gap in the original nine: the job description's
"Content Conversion and Production" responsibilities — translating faculty
and SME research into client-ready, multi-format assets (decks, toolkits,
infographics, blog posts) with version control, QA, and release discipline
— weren't cleanly owned by Donham (pedagogical frameworks), Levitt
(external growth marketing), or Land (video/audio production).

Real tools as of 2026-09-03, both verified live: Canva (mcp__Canva__*) and
Gamma (mcp__Gamma__*, verified via a real get_themes call). Gamma can only
create new generations, not edit existing ones — send Kaitlyn to the
Gamma editor for revisions. Version control runs through outputs/, not a
separate tool — see config.yaml's version_control_mechanism note.
"""
from agents.base_director import BaseDirector, DirectorOutput


class ContentProductionDirector(BaseDirector):
    director_id = "content_production"
    namesake = "Copeland"
    title = "Director of Content Conversion & Production — the Copeland Desk"
    model_ref = "anthropic_pro.chat"

    keywords = [
        "convert", "conversion", "deck", "toolkit", "infographic",
        "client-ready", "market-facing", "release", "version control",
        "qa process", "consistency", "asset", "translate research",
        "one-pager", "handout", "canva", "gamma",
    ]

    system_prompt = (
        "You are the Director of Content Conversion & Production at the HBS "
        "AI Institute. You convert faculty and subject-matter-expert research "
        "into client-ready, market-facing, multi-format assets: facilitation "
        "decks, toolkits, infographics, blog posts, and other digital content "
        "— translating complex academic material into accessible, "
        "participant-centered formats. Two real, connected tools generate "
        "these for real as of 2026-09-03 (both verified live): Canva "
        "(brand-kit consistency, export flexibility) and Gamma (fast, "
        "theme-driven first drafts — but it can only create new "
        "generations, never edit an existing one, so send Kaitlyn to the "
        "Gamma editor for revisions). You also own version control, QA, "
        "and release documentation across all learning materials — every "
        "released asset goes to outputs/<date>-<slug>/ with a README and "
        "gets committed, which is the actual version-control mechanism, "
        "not a separate tool. You do not design the pedagogical framework "
        "(that's Donham) or write external growth/marketing copy (that's "
        "Levitt) — you take material that already exists and turn it into "
        "a specific, polished, released deliverable. Always name the "
        "source material you're converting from and the target format(s) "
        "you're producing."
    )

    def handle(self, task: str, context: str = "") -> DirectorOutput:
        output = super().handle(task, context)
        # Anything released/shipped to learners or externally still needs
        # the pedagogical review or external-publish checkpoint upstream —
        # this Director drafts and version-controls, it doesn't self-approve.
        if output.requires_hitl is None:
            output.requires_hitl = "pedagogical_review"
        return output
