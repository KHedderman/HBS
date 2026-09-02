# KH HBS Agentic Workforce — web front end

`docket.html` is the published-Artifact source for **KH HBS Agentic
Workforce**, the visual/interactive face of the multi-agent system,
directed by Kaitlyn Hedderman:
https://claude.ai/code/artifact/e2a1d047-54f9-42c4-bdcc-19d3d3c26594

It's an HBS-branded dashboard that:

- Renders the hub-and-spoke architecture as a live, draggable 3D scene
  (Exhibit A) — the Chief of Staff hub with the ten Directors orbiting it.
- Lets you send the team a request directly on the page. Submitting calls
  Claude via the artifact's `sample` capability (billed to *your* Claude
  usage — no separate API key, no metered cost) using a prompt built from
  the same Director roster and governance rules as `config.yaml`, and
  writes the result to the artifact's own `db` capability — a shared, live
  document store scoped to this artifact.
- Shows every request in the Work Log: which Directors were dispatched and
  why, the drafted output, any HITL flags (strategic, pedagogical,
  cost-bearing, external-publish), and an Approve / Needs Revision control
  you work through by hand.
- Flags — rather than fakes — anything that needs a live connector
  (a real Lovable build, real ElevenLabs audio, a Granola transcript
  pull). Those can only run from a live chat session with Claude, so a
  flagged request tells you what to bring back to chat instead of
  pretending to have done it.

## What this is *not*

- It is **not** wired to Lovable, ElevenLabs, Granola, or Notion directly —
  those connectors are authenticated to a chat session, not to a published
  web page. This page is honest about that boundary rather than faking it.
- It does **not** read or write the repo's `memory/`, `qa_logs/`, or
  Airtable pipeline directly — its Work Log is its own record, stored in
  the artifact's database, separate from what `agents/memory_curator.py`
  and `pipelines/pipeline_tracker.py` persist when you work through a chat
  session instead. Claude can add matching entries here after a chat
  session on request, so the two logs can be kept in sync manually.
- It does **not** change `config.yaml`'s `operating_mode` — sending a
  request here is still an attended action (you're the one clicking the
  button and reviewing the result); it has no path to true unattended
  execution.

## Updating it

Edit `docket.html`, then republish it to the same Artifact URL above
(pass that URL to the Artifact tool rather than publishing fresh) so the
link stays live.
