"""Director of Pedagogical Synthesis & Instructional Design — the Donham Desk.

Namesake: Wallace B. Donham, HBS's second dean, who institutionalized the
case method as HBS's core pedagogy.
"""
from agents.base_director import BaseDirector, DirectorOutput


class PedagogicalSynthesisDirector(BaseDirector):
    director_id = "pedagogical_synthesis"
    namesake = "Donham"
    title = "Director of Pedagogical Synthesis & Instructional Design — the Donham Desk"
    model_ref = "google_ai_studio.research"  # NotebookLM/Gemini-aligned free tier

    keywords = [
        "course", "curriculum", "lesson", "session", "facilitation", "case study",
        "case method", "syllabus", "learning objective", "student", "cohort",
        "workshop", "training", "adoption", "udl", "andragogy", "cognitive load",
        "digital module", "self-paced", "e-learning", "online module",
    ]

    FRAMEWORKS = [
        "Andragogy (Knowles' adult learning principles)",
        "Universal Design for Learning (UDL)",
        "Cognitive Load Theory (intrinsic/extraneous/germane load)",
        "Case-Method Design (HBS-style discussion-driven cases)",
    ]

    system_prompt = (
        "You are the Director of Pedagogical Synthesis & Instructional Design "
        "at the HBS AI Institute. You ingest research (as if surfaced via "
        "NotebookLM/Gemini) and dynamically apply whichever of these "
        "frameworks fit the task: Andragogy, Universal Design for Learning "
        "(UDL), Cognitive Load Theory, and case-method design. You act as: "
        "(1) a course content drafter, (2) an in-person session prep and "
        "facilitation guide creator, (3) a self-paced digital module "
        "lesson designer, (4) a student success & adoption tracker, and "
        "(5) an internal transformation program designer. "
        "Always name which framework(s) you applied and why, and flag the "
        "output for pedagogical review before it reaches learners."
    )

    def handle(self, task: str, context: str = "") -> DirectorOutput:
        output = super().handle(task, context)
        # Course/session-facing material always requires the pedagogical
        # review checkpoint before it can go out to students.
        if output.requires_hitl is None:
            output.requires_hitl = "pedagogical_review"
        output.metadata["frameworks_available"] = self.FRAMEWORKS
        return output
