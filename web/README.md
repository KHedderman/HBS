# KH HBS Agentic Workforce — web front end

`workforce.html` is the published-Artifact source for **KH HBS Agentic
Workforce**, the visual/interactive face of the multi-agent system,
directed by Kaitlyn Hedderman:
https://claude.ai/code/artifact/e2a1d047-54f9-42c4-bdcc-19d3d3c26594

## Design

Chat-first, not chart-first. An earlier version led with a 3D draggable
hub-and-spoke visualization — it didn't work as an actual interface and
was replaced entirely. The current layout is a plain, familiar SaaS
pattern:

- **Left sidebar** — brand, a nav list (Chat + five category tabs), and a
  collapsible plain-text roster of Eliot, Winsor, and the ten Directors.
- **Chat tab (home)** — a real conversation thread with Eliot: your
  request on the right, his synthesized reply on the left showing which
  Director(s) handled it and why, any HITL flags, and Approve / Needs
  Revision / Delete controls. The composer has a mic button (browser
  Web Speech API — no external service, hidden if unsupported) alongside
  the text box.
- **Category tabs** — Market Intelligence, Course Drafts, PRDs & GitHub
  Sync, Pipeline Tracker, Analytics — each filters the same saved records
  to whichever ones a matching Director touched, so a course draft shows
  up under Course Drafts without you hunting for it in one long feed.

## How it works

- Submitting calls Claude via the artifact's `sample` capability (billed
  to *your* Claude usage — no separate API key, no metered cost) using a
  prompt built from the same Director roster and governance rules as
  `config.yaml`.
- The result is written to the artifact's own `db` capability — a shared,
  live document store scoped to this artifact, collection `requests`.
  Everything persists across reloads; nothing disappears except by an
  explicit Delete click (with a confirm prompt).
- Flags — rather than fakes — anything that needs a live connector (a
  real Lovable build, real ElevenLabs/Replicate video or audio, a Granola
  transcript pull, a live GitHub/Notion/Airtable write). Those can only
  run from a live chat session with Claude, so a flagged request tells
  you what to bring back to chat instead of pretending to have done it.

## What this is *not*

- It is **not** wired to Lovable, ElevenLabs, Replicate, Granola, GitHub,
  Notion, or Airtable directly — those are either chat-session
  connectors or require a real backend of your own; a published web page
  has neither. This page is honest about that boundary rather than
  faking it.
- It does **not** read or write the repo's `memory/`, `qa_logs/`, or
  Airtable pipeline directly — its saved requests are their own record,
  separate from what `agents/memory_curator.py` and
  `pipelines/pipeline_tracker.py` persist when you work through a chat
  session instead. Claude can add matching entries here after a chat
  session on request, so the two logs can be kept in sync manually.
- It does **not** change `config.yaml`'s `operating_mode` — sending a
  request here is still an attended action (you're the one clicking the
  button and reviewing the result); it has no path to true unattended
  execution.
- It is **not** an independent product — it's still hosted on
  `claude.ai`, under your Claude account. A fully independent, separately
  hosted product (its own domain, real connector execution) is what the
  parallel Lovable build is for, when/if that's finished.

## Updating it

Edit `workforce.html`, then republish it to the same Artifact URL above
(pass that URL to the Artifact tool rather than publishing fresh) so the
link stays live.
