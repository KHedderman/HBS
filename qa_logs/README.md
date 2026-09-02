# QA Logs

This directory holds the system's audit trail. Two files are generated
automatically at runtime (not committed with seed content, but tracked once
they exist):

- `routing_log.jsonl` — every Intelligent Router decision (not yet wired to
  auto-log; add a call to it in `agents/chief_of_staff.py::_route` if you
  want a persistent routing audit trail beyond memory's session logs).
- `hitl_decision_log.jsonl` — every Human-in-the-Loop checkpoint raised, and
  how it was resolved (approved/denied, or the cost-governance choice made).
  Written by `agents/hitl.py`.

`accessibility_audit_template.md` is the template the Director of
Accessibility & Compliance fills out per artifact — see that file.
