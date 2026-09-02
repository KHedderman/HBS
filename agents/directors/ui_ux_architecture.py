"""Director of Interactive UI/UX Architecture — the Gropius Desk.

Namesake: Walter Gropius, Harvard GSD professor and Bauhaus founder — an
actual architecture pioneer (cross-school pun intended).

Two execution paths, both governed by the same gate:
  - Standalone script (this class): no Lovable API access — always produces
    a spec + a ready-to-paste Lovable build prompt for a human to run.
  - Interactive chat mode: with the Lovable connector connected, Claude
    (embodying this Director) CAN call mcp__Lovable__create_project /
    send_message directly to produce a real, live build — but every such
    call spends Lovable workspace credits, so it clears a cost_bearing_action
    checkpoint with the user first, every time, not just on the first build.
"""
from agents.base_director import BaseDirector


class UIUXArchitectureDirector(BaseDirector):
    director_id = "ui_ux_architecture"
    namesake = "Gropius"
    title = "Director of Interactive UI/UX Architecture — the Gropius Desk"
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
        "with state/props, (4) a ready-to-paste Lovable build prompt. In an "
        "interactive chat session with the Lovable connector connected, "
        "offer to send that prompt to Lovable directly and build the real "
        "thing — but only after the user confirms, since every Lovable "
        "message spends their workspace credits."
    )
