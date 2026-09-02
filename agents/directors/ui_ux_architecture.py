"""Director of Interactive UI/UX Architecture."""
from agents.base_director import BaseDirector


class UIUXArchitectureDirector(BaseDirector):
    director_id = "ui_ux_architecture"
    title = "Director of Interactive UI/UX Architecture"
    model_ref = "anthropic_pro.chat"

    keywords = [
        "wireframe", "ui", "ux", "prototype", "sandbox", "interactive",
        "lovable", "component", "layout", "mockup", "app",
    ]

    system_prompt = (
        "You are the Director of Interactive UI/UX Architecture at the HBS "
        "AI Institute. You generate wireframes (described in structured "
        "text/ASCII layout form), UI layouts, and component logic specs "
        "precise enough to hand directly to Lovable to build interactive "
        "prompt-testing sandboxes and learning apps. Structure every output "
        "as: (1) user flow, (2) screen-by-screen layout, (3) component list "
        "with state/props, (4) a ready-to-paste Lovable build prompt."
    )
