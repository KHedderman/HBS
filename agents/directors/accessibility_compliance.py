"""Director of Accessibility & Compliance."""
from agents.base_director import BaseDirector, DirectorOutput


class AccessibilityComplianceDirector(BaseDirector):
    director_id = "accessibility_compliance"
    title = "Director of Accessibility & Compliance"
    model_ref = "anthropic_pro.fast"

    keywords = [
        "accessibility", "compliance", "audit", "reading level", "wcag",
        "cognitive load", "universal design", "alt text", "captions",
    ]

    system_prompt = (
        "You are the Director of Accessibility & Compliance at the HBS AI "
        "Institute. You audit all generated materials against: universal "
        "design standards (WCAG-aligned), estimated reading level "
        "(Flesch-Kincaid grade band), and cognitive load thresholds "
        "(chunking, working-memory load, extraneous complexity). Always "
        "return a pass/fail per criterion with the specific fix required — "
        "never a vague 'looks fine'. This audit is the last gate before any "
        "learner-facing material ships."
    )

    def audit(self, material: str) -> DirectorOutput:
        task = (
            "Audit the following material. Return a table with columns: "
            "Criterion | Pass/Fail | Fix Required, covering at minimum: "
            "WCAG universal design, reading level, cognitive load.\n\n"
            f"MATERIAL:\n{material}"
        )
        return self.handle(task)
