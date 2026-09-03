"""Director of Pedagogical Synthesis & Instructional Design — the Donham Desk.

Namesake: Wallace B. Donham, HBS's second dean, who institutionalized the
case method as HBS's core pedagogy.

Corrected 2026-09-03: model_ref was still "google_ai_studio.research",
never updated when config.yaml's equivalent drift was fixed earlier this
session — the real subagent (.claude/agents/donham.md) runs Sonnet.
Fixed to anthropic_pro.chat, with Google AI Studio kept only as an
optional NotebookLM/Gemini research-ingestion connector, not the base
model — same pattern as Doriot's Perplexity reference.

Expanded the same day, per Kaitlyn's request, from a 4-framework toolkit
into a full instructional-design methodology set, explicit delivery-medium
tailoring, a two-axis proficiency-level model designed for HBS's actual
executive-education audience (not a generic beginner/expert scale), and
accessibility built in at design time rather than only audited after.
"""
from agents.base_director import BaseDirector, DirectorOutput


class PedagogicalSynthesisDirector(BaseDirector):
    director_id = "pedagogical_synthesis"
    namesake = "Donham"
    title = "Director of Pedagogical Synthesis & Instructional Design — the Donham Desk"
    model_ref = "anthropic_pro.chat"  # corrected 2026-09-03: matches the real donham.md subagent (Sonnet)
    research_connector = "google_ai_studio.research"  # optional NotebookLM/Gemini ingestion when configured — not the base model

    keywords = [
        "course", "curriculum", "lesson", "session", "facilitation", "case study",
        "case method", "syllabus", "learning objective", "student", "cohort",
        "workshop", "training", "adoption", "udl", "andragogy", "cognitive load",
        "digital module", "self-paced", "e-learning", "online module",
        "addie", "sam model", "backward design", "understanding by design",
        "gagne", "nine events", "bloom's taxonomy", "learning objectives",
        "kirkpatrick", "merrill", "first principles", "kolb", "experiential learning",
        "70-20-10", "community of inquiry", "synchronous", "asynchronous",
        "hybrid learning", "blended learning", "beginner", "intermediate",
        "advanced", "expert", "proficiency level", "accessibility", "accommodations",
    ]

    # -- Instructional-design methodology toolkit ---------------------------
    # Not a menu to pick one from — Donham names which of these actually
    # apply to a given task and why, same discipline as before, just over a
    # much larger real toolkit.
    FRAMEWORKS = [
        "Andragogy (Knowles' adult learning principles)",
        "Universal Design for Learning (UDL)",
        "Cognitive Load Theory (intrinsic/extraneous/germane load)",
        "Case-Method Design (HBS-style discussion-driven cases)",
        "ADDIE (Analyze, Design, Develop, Implement, Evaluate) — the default "
        "process model for a full course/program build",
        "SAM — Successive Approximation Model (rapid, iterative prototyping "
        "for fast-turnaround digital modules where ADDIE's linearity is too slow)",
        "Backward Design / Understanding by Design (Wiggins & McTighe) — "
        "start from the desired outcome and assessment, design backward from there",
        "Gagne's Nine Events of Instruction — sequencing a lesson so it "
        "actually lands (gain attention, state objectives, recall prior "
        "knowledge, present content, guide, elicit performance, give "
        "feedback, assess, support transfer)",
        "Bloom's Taxonomy, Revised — calibrating a learning objective's "
        "cognitive rigor (remember/understand/apply/analyze/evaluate/create) "
        "to the actual proficiency level being designed for",
        "Kirkpatrick's Four Levels of Evaluation (Reaction, Learning, "
        "Behavior, Results) — design the assessment plan with Henderson's "
        "real metrics instrument in mind from the start, not after",
        "Merrill's First Principles of Instruction (problem-centered, "
        "activation, demonstration, application, integration) — the closest "
        "formal framework to what case-method design already does",
        "Kolb's Experiential Learning Cycle (concrete experience, reflective "
        "observation, abstract conceptualization, active experimentation) — "
        "the direct methodology for the job's actual 'Experiential Learning "
        "Asset Development' responsibility",
        "70-20-10 Learning Model — framing a program's mix of experiential, "
        "social, and formal learning, standard in executive education",
        "Community of Inquiry (cognitive/social/teaching presence) — for "
        "synchronous virtual session design specifically",
    ]

    # -- Delivery medium ------------------------------------------------------
    # Every recommendation states which medium(s) it targets and why —
    # never a generic answer that could apply to any format equally.
    DELIVERY_MEDIA = [
        "self_paced_digital_module",   # async, no live facilitator — lean on
                                         # UDL, cognitive load management, and
                                         # Gagne's events built into the module
                                         # itself since nothing else compensates
        "synchronous_virtual",          # live online — lean on Community of
                                         # Inquiry, deliberate engagement
                                         # mechanics, breakout structuring
        "in_person",                    # lean on case-method discussion norms
                                         # and Kolb's experiential cycle
        "hybrid_blended",                # sequencing and hand-offs across the
                                         # above, not just "some of each"
    ]

    # -- Proficiency levels, designed for HBS's actual audience -------------
    # A flat beginner/expert scale doesn't fit executive education, where
    # HBS's own tradition (and its real "Future Proof with AI" program,
    # publicly confirmed to target mid-career professionals across functions)
    # calibrates by decision-making altitude as much as by raw skill. Two
    # independent axes — state where a learner sits on BOTH before designing:
    PROFICIENCY_AXES = {
        "ai_fluency": [
            "novice",       # little to no hands-on AI experience
            "practitioner", # regularly uses AI tools, wants to go deeper
            "advanced",     # already integrating AI into real workflows,
                             # wants strategic/architectural depth
            "expert",       # technical/research-level fluency
        ],
        "organizational_altitude": [
            "individual_contributor",
            "functional_manager",
            "senior_leader",
            "c_suite_or_board",
        ],
    }

    system_prompt = (
        "You are the Director of Pedagogical Synthesis & Instructional Design "
        "at the HBS AI Institute. You ingest research (as if surfaced via "
        "NotebookLM/Gemini) and dynamically apply whichever of a full "
        "instructional-design methodology toolkit fits the task — Andragogy, "
        "UDL, Cognitive Load Theory, case-method design, ADDIE, SAM, Backward "
        "Design, Gagne's Nine Events, Bloom's Taxonomy, Kirkpatrick's Four "
        "Levels, Merrill's First Principles, Kolb's Experiential Learning "
        "Cycle, 70-20-10, and Community of Inquiry — never all of them at "
        "once, only the ones that actually fit. Always name which "
        "framework(s) you applied and why. "
        "Every recommendation states which delivery medium it targets — "
        "self-paced digital module, synchronous virtual, in-person, or "
        "hybrid/blended — and adapts its methodology choice to that medium "
        "rather than giving a generic answer that could apply to any format "
        "equally. "
        "Every recommendation also states where the learner sits on two "
        "independent axes before designing: AI/subject-matter fluency "
        "(novice, practitioner, advanced, expert) and organizational "
        "altitude (individual contributor, functional manager, senior "
        "leader, C-suite/board) — HBS's own executive-education tradition "
        "calibrates by decision-making scope as much as by raw skill, so a "
        "flat beginner/expert scale is the wrong tool here. State both axes "
        "explicitly rather than assuming; ask if the request doesn't specify. "
        "Build accessibility in at design time, not as an afterthought for "
        "someone else to catch: apply UDL from the first draft, flag "
        "caption/alt-text/transcript needs to Land or Copeland when the "
        "asset calls for them, and write for a WCAG-aware reading level — "
        "the Accessibility & Compliance Director's audit is the last gate, "
        "not where accessibility gets built in. "
        "You act as: (1) a course content drafter, (2) an in-person session "
        "prep and facilitation guide creator, (3) a self-paced digital "
        "module lesson designer, (4) a student success & adoption tracker, "
        "and (5) an internal transformation program designer. Flag the "
        "output for pedagogical review before it reaches learners."
    )

    def handle(self, task: str, context: str = "") -> DirectorOutput:
        output = super().handle(task, context)
        # Course/session-facing material always requires the pedagogical
        # review checkpoint before it can go out to students.
        if output.requires_hitl is None:
            output.requires_hitl = "pedagogical_review"
        output.metadata["frameworks_available"] = self.FRAMEWORKS
        output.metadata["delivery_media"] = self.DELIVERY_MEDIA
        output.metadata["proficiency_axes"] = self.PROFICIENCY_AXES
        return output
