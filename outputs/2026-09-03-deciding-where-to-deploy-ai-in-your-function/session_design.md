# Session Design: "Deciding Where to Deploy AI in Your Function"

**Format:** 90-minute in-person session, HBS AI Institute executive education program
**Director:** Donham (Pedagogical Synthesis & Instructional Design)

Two verification notes before the design, per this workforce's standing rules:

- **Connector check (live, not assumed):** Granola shows `connected: true` in the connector list but returned `Unauthorized: user has not created a Granola account yet` when queried for prior session context on this cohort/program. So this design draws on the request brief and the repo's real instructional-design assets (`ROLE_CONTEXT.md`, `metrics/README.md`, the empty `metrics/learning_metrics.jsonl`) — not on any actual meeting notes, because none were retrievable. If real cohort intake notes exist somewhere, hand them to me and I'll recalibrate the case and canvas to the actual functions/industries represented.
- **The case vignette below is an original teaching scenario I've written for this session, not a real, published, or licensed company.** No case-library or HBS Publishing connector is available in this session to source an actual HBS case, so I built a discussion-ready illustrative one instead. If the program wants a real licensed HBS case in this slot, that's a sourcing task outside this workforce's current connectors — flag to Doriot for research support, or license one through HBS Publishing directly.

---

## 1. Learner calibration (both axes, stated per design policy)

- **AI/subject-matter fluency: Practitioner.** These VPs use AI tools regularly in their own work. Do *not* spend room time on what AI is or basic tool literacy — that would waste practitioner time and insult the room. The gap is specifically **leading deployment decisions**, not using the tools.
- **Organizational altitude: Senior leader (VP, functional).** They own a P&L or functional scope, not a single task. The decisions this session prepares them for are portfolio-level ("which 2-3 things in my function, out of 20 candidates") and have to be **defended upward** (to a C-suite/board they report into) and **translated downward** (to teams who'll execute). This is different from an IC's task-selection problem or a C-suite's enterprise-portfolio problem — the design targets *that* altitude specifically.

**Consequence for design:** skip novice tool-adoption content; go straight to a decision-quality problem. Success looks like a defensible, criteria-based prioritization they can walk into their next leadership meeting with — not a list of "cool AI use cases."

## 2. Frameworks applied, and why (only these — not the full catalog)

| Framework | Why it applies here |
|---|---|
| **Backward Design (Wiggins & McTighe)** | Started from the artifact each VP must leave with (a defensible draft prioritization for one real process) and designed every minute backward from that, rather than starting from content to cover. |
| **Case-Method Design** | In-person + senior peer audience is exactly what case discussion is built for: surface reasoning, expose disagreement, avoid the facilitator lecturing practitioners on things they already do. |
| **Kolb's Experiential Learning Cycle** | In-person sessions should use the room, not just talk at it. Concrete experience (case) → reflective observation (discussion) → abstract conceptualization (framework) → active experimentation (applying it to their own function) is the literal shape of the 90 minutes below. |
| **Gagné's Nine Events** | Used to sequence the run-of-show so attention, activation, guided practice, and transfer are each deliberately built in, not left to chance. |
| **Bloom's Taxonomy (Revised)** | Objectives are pinned at Analyze/Evaluate, with a Create stretch (the draft canvas) — appropriate for practitioner-level, senior-leader learners. No Remember/Understand-level objectives; this audience doesn't need them. |
| **Cognitive Load Theory** | The case is assigned as pre-work specifically to move first-exposure reading (intrinsic load) out of the room, so all 90 in-room minutes go to germane load — applying and defending, not absorbing facts for the first time. |
| **Andragogy (Knowles)** | VPs' own functional experience is treated as the primary teaching resource (small groups built around their real processes), the problem is self-selected and immediately relevant, and the framework is optional scaffolding, not a mandate. |
| **Kirkpatrick's Four Levels** | Assessment plan below is built against this from the start, mapped to Henderson's real (currently empty) `metrics/learning_metrics.jsonl` schema — not bolted on after. |

Not used: UDL is applied as a design-time practice (see §6) rather than named as a driving framework; Community of Inquiry doesn't apply (this isn't synchronous virtual); 70-20-10 and SAM/ADDIE are program-level concerns above a single session.

## 3. Learning objectives (Bloom-calibrated)

By the end of the session, each participant will be able to:

1. **Evaluate** a candidate AI use case in their function against a shared value/feasibility/risk framework, distinguishing genuine deployment-readiness from surface novelty. *(Evaluate)*
2. **Analyze** why two organizations with access to comparable AI capability made divergent deployment choices, identifying which contextual factors — data readiness, process variability, risk exposure, workforce readiness — actually drove the divergence. *(Analyze)*
3. **Produce** a defensible, one-page draft prioritization of AI deployment candidates for one real process in their own function, using the shared framework. *(Create — stretch objective)*
4. **Articulate**, in terms a non-technical board member would accept, why that prioritization is right — not just what it is. *(Evaluate, tied directly to the "defend upward" demand of VP altitude)*

---

## 4. Pre-work (sent 5-7 days out — required, and load-bearing for the design)

Sending this out is what makes 90 minutes enough. Skipping it collapses the design back into a lecture.

1. **The case** (below), ~10-minute read.
2. **The AI Deployment Decision Canvas** (one page, §7) — each VP arrives with Section 1 pre-filled for **one real candidate process in their own function**. This is the single hardest pre-work ask and the one facilitators must chase down; a participant who shows up without a real process to work is functionally not present for the last third of the session.
3. One line of framing: *"You'll leave with a working draft, not a finished plan. Bring your most contested candidate, not your safest one."* — this primes psychological safety for genuine debate later (see case-method norms, §6).

### The case: *Northfield Retail Group*

*(Original teaching vignette written for this session — not a real company.)*

Northfield Retail Group is a $2.4B mid-market apparel and home-goods retailer, 340 stores plus e-commerce, facing margin pressure from a discount competitor and a activist board member pushing for "an AI strategy" within two quarters. The CEO has asked three functional VPs to each bring one AI deployment proposal to the next board meeting. All three have access to the same enterprise LLM platform IT just licensed.

- **VP of Customer Care (Elena Ruiz)** wants to deploy an AI agent to handle the 40% of contact-center tickets that are order-status and return questions. Data is clean (structured order history), the process is highly repetitive, and a competitor already does this — but her team is already stretched thin from a recent RIF, and the union contract requires 60 days' notice on any role-impacting change. Ruiz has run a 3-week pilot with strong containment rates but has not yet modeled the change-management timeline.
- **VP of Merchandising (David Okafor)** wants to deploy AI-assisted demand forecasting for seasonal buys — the highest financial upside of the three ($18-30M in reduced markdowns, by his estimate), but Northfield's SKU-level sales data is fragmented across two legacy systems from a five-year-old acquisition that was never fully integrated, and the forecasting models a vendor demoed assumed clean, unified data that doesn't exist. Okafor is confident the data problem is "mostly solved" based on a vendor's assurances; his own data team says 6-9 months of remediation work remain.
- **VP of HR (Priya Anand)** wants to deploy an AI screening tool to cut time-to-hire for hourly store staff, currently Northfield's most acute operational pain point (140 unfilled store roles nationwide). The tool is cheap and fast to stand up, but Anand's team has not yet reviewed it for adverse-impact/disparate-treatment risk under EEOC guidance, and two peer retailers have had public incidents with biased hiring-AI tools in the past 18 months.

All three VPs believe their proposal is the strongest. The CEO has room to fund only one pilot before the board meeting.

*(Facilitators: this is intentionally under-specified — e.g., no explicit cost figures for Ruiz's pilot, no named vendor for Okafor. That's deliberate; case discussion should surface what information the room thinks is missing before jumping to a verdict.)*

---

## 5. In-room run of show (90 minutes, Gagné-sequenced)

| Time | Segment | Gagné event(s) | Kolb stage |
|---|---|---|---|
| 0:00–0:05 | **Open / hook** — facilitator opens with a single contrast: two real, publicly reported examples of the *same* AI capability deployed well in one company's function and disastrously in another's (facilitator's choice, kept current). No case discussion yet — just: "same technology, opposite outcomes. Why?" | Gain attention | — |
| 0:05–0:10 | **State objectives + activate prior knowledge** — objectives from §3 shown; one-word round: "name the deployment decision you're personally least sure about right now." No discussion, just captured on the board — it gets revisited at 0:80. | State objectives, recall prior learning | Concrete experience begins |
| 0:10–0:40 | **Case discussion (cold-call, Socratic)** — see discussion plan below. | Present content (via discussion, not lecture), provide guidance | Concrete experience → Reflective observation |
| 0:40–0:50 | **Framework crystallization** — facilitator distills the board work (not a pre-built slide dump) into the named decision framework: a **Value × Readiness matrix with a Risk gate** (detail below). | Present the organizing content | Abstract conceptualization |
| 0:50–1:10 | **Small-group application** — groups of 3-4, mixed by function, using each VP's pre-filled Canvas Section 1 for their *own* real process. | Elicit performance, provide guidance | Active experimentation |
| 1:10–1:20 | **Cross-functional pressure test** — 2 groups report out; room + facilitator stress-test against the framework's criteria, out loud. | Elicit performance, provide feedback | Active experimentation (continued) |
| 1:20–1:27 | **Synthesis + commitment** — facilitator names 2-3 patterns/failure modes seen live in the room's own groups (not generic); each VP writes one specific, dated commitment. | Assess performance, enhance retention/transfer | Reflective observation (loop closes) |
| 1:27–1:30 | **Close + pulse-check** — 2-question form (Kirkpatrick L1/L2, see §8). | Assess performance | — |

### Case discussion plan (0:10–0:40) — facilitator's board plan

**Opening question (cold-call, not volunteer):** *"If you were the CEO and could fund exactly one pilot, which one, and why?"* Call on 3 participants by name in sequence, capture positions on the board as three columns (Ruiz / Okafor / Anand), one line each — force a real position before nuance is allowed in.

**Second wave (open discussion, facilitator pushes contrarian views):**
- "What does each VP's own confidence in their proposal *not* tell you about its actual deployment-readiness?" — surfaces the difference between advocacy and evidence (Okafor's forecasting case is the trap here: highest upside, most fragile foundation).
- "Ruiz has the cleanest data and a completed pilot — why might that still not make hers the right first move?" — surfaces change-management and labor-relations risk as a real cost, not a footnote.
- "Anand's problem is the most operationally urgent. Does urgency belong in this framework, and if so, where?" — surfaces the tension between "important" and "ready," which is the whole point of the session.

**Board layout:** as criteria surface organically from the room (data readiness, financial upside, risk/compliance exposure, change-management cost, urgency), write them down as they're named — do **not** pre-populate the board with the framework's criteria before the room generates them. The framework in the next segment should feel like *the room's own words, organized*, not a slide imposed on the discussion. This is the case-method discipline: the facilitator's authority in this segment is discussion design, not content delivery.

**Case-method discussion norms to state at 0:10, before opening:** disagree with the position, not the person; "I don't have enough information to decide" is a legitimate answer if you can name what's missing; nothing said about a peer's own function leaves the room. State this explicitly — this room is senior peers who may compete for the same enterprise resources back home, and psychological safety has to be actively built, not assumed.

### The framework (crystallized at 0:40-0:50)

**Value × Readiness matrix, with a Risk gate:**
- **Value (x-axis):** magnitude of financial/strategic upside if it works.
- **Readiness (y-axis):** composite of data quality, process stability, and organizational capacity to absorb the change — *not* technical feasibility alone.
- **Risk gate (applied before plotting, not after):** any candidate with an unresolved legal/compliance/reputational exposure (Anand's adverse-impact question is the case's example) doesn't get plotted until that gate clears — high value and high readiness don't override an open risk gate, they just mean the gate needs to clear *fast*.

Northfield's three candidates, once plotted, typically land: Ruiz (high readiness, moderate value, moderate transition risk) as the defensible first pilot; Okafor (high value, low actual readiness behind an optimistic self-report) as "fix the foundation first, don't pilot yet"; Anand (highest urgency, ungated risk) as "gate must clear before this is even on the matrix." The discussion should get the room to this on its own — the facilitator names it, doesn't reveal it as a twist.

---

## 6. Accessibility and UDL, built in now (not audited in later)

- Pre-work and the Canvas sent as an accessible, screen-reader-clean document (not a scanned PDF or image-only slide) at least 5 days out — flag to Copeland for production/QA.
- Case discussion uses cold-call by name with advance notice of the norms (§5) rather than surprise put-on-the-spot questioning, which serves both engagement and accessibility for participants who process better with preparation time.
- Room materials: high-contrast board work, large-print canvas copies available on request, and the framework restated verbally as well as written on the board (dual-coding, not reliance on visual-only).
- No video/audio assets in this session as designed, so no captioning need currently — if the "hook" examples in §5 end up using a video clip, flag to Land for captions before use.
- Small groups mixed by function, not self-selected, to prevent any one VP being isolated by role or seniority difference within the cohort.

---

## 7. AI Deployment Decision Canvas (one page — pre-work + in-room tool)

| Field | Prompt |
|---|---|
| Process/decision candidate | The one real process you're evaluating |
| Current pain (in your words, not AI's) | What's actually broken or costly today |
| Data readiness | Clean/structured, fragmented, or unknown — be honest, not optimistic |
| Feasibility path | Build, buy, or adapt an existing tool |
| Estimated value magnitude | Rough order of magnitude — doesn't need to be precise |
| Risk/compliance flags | Anything that would gate this before a pilot can start |
| Change-management cost | Who has to change how they work, and how hard is that |
| Decision | Pilot within 30/90 days / gate must clear first / park it — and why |

Section 1 (Process through Change-management cost) is pre-work. "Decision" is filled in-room during the small-group segment, after peer pressure-testing.

---

## 8. Assessment approach (Kirkpatrick, mapped to Henderson's real instrument)

Checked directly: `metrics/learning_metrics.jsonl` currently has **0 entries** — no program has been run yet, so nothing below is a report of existing data. This is the collection design for this session, to be logged into that real file once it's actually delivered, using the schema in `metrics/README.md` (`timestamp, program, metric, value, source, notes`).

| Kirkpatrick level | What's measured here | Mechanism | Maps to `learning_metrics.jsonl` metric |
|---|---|---|---|
| **1 — Reaction** | Session-level satisfaction | 1-5 rating + one open-text ("what will you use Monday") on the 0:27–0:30 close-out form | `session_satisfaction` |
| **2 — Learning** | Self-rated confidence shift | Single item — *"How confident are you in your ability to decide where to deploy AI in your function?"* (1-7) — asked once in the pre-work and once at close; the delta is the metric | `knowledge_delta` |
| **2 (facilitator lens)** | Discussion quality/engagement | Facilitator's own post-session rating, filled immediately after | `facilitator_engagement_rating` |
| **3 — Behavior** | Whether the draft Canvas actually gets socialized/acted on back at work | **Not observable in the room.** Requires a 30-day async follow-up — recommend one short email/form asking whether the "Decision" field on their Canvas actually moved (pilot started / gated / parked, and why) | Not yet a field — flag to Henderson as a gap |
| **4 — Results** | Whether the pilot they picked produced a real outcome | **Not observable at all within this session's scope.** Requires a 90-day follow-up tied to the specific process each VP named — a program-level tracking commitment, not a single-session one | Not yet a field — flag to Henderson |
| — | Completion / time-to-competency | Not meaningful for a single 90-minute module; relevant at full-program level only | `completion_rate`, `time_to_competency` — N/A here |

**Honest gap, flagged rather than papered over:** this design closes Level 1/2 within the room but cannot close Level 3/4 on its own — that requires Taylor (program ops, to actually schedule and send the 30/90-day follow-ups) and Henderson (to add the behavior/results fields this session surfaces a need for) to build the follow-up mechanism. Recommend this get raised as a real roster action item, not left implicit.

---

## 9. HITL flag

Per `config.yaml`'s `hitl_checkpoints`, this session design requires **`pedagogical_review`** before it goes to a facilitator or reaches learners — this has not happened yet. Specifically worth a second set of eyes on: (a) whether the Northfield vignette's fictional-but-plausible compliance/HR content (adverse-impact risk) needs legal review given this is going to a live executive audience, and (b) whether the facilitator running this has genuine case-method cold-call experience, since the design's Kolb/Gagné sequencing depends on that skill specifically.

---

## Transparency note

**Director engaged:** Donham (Pedagogical Synthesis & Instructional Design), sole author of this design.
**Frameworks applied:** Backward Design, Case-Method Design, Kolb's Experiential Learning Cycle, Gagné's Nine Events, Bloom's Taxonomy (Revised), Cognitive Load Theory, Andragogy, Kirkpatrick's Four Levels — named and reasoned above in §2, not the full catalog.
**Models/tools actually used:** Claude Sonnet 5 reasoning only (Donham's designated model per `.claude/agents/donham.md`), included in Kaitlyn's existing Claude subscription — no metered API cost. `ListConnectors` and a live Granola query were run and returned Unauthorized (see top of this response) — no external meeting data was actually retrieved despite the connector showing as connected. No case-library, research, video, or design connector was used to produce this content.
**Sources:** The named frameworks (Wiggins & McTighe, Gagné, Bloom, Kirkpatrick, Kolb, Knowles) are established public academic theory, not proprietary or live-sourced content — no citation link applies. The Northfield case is original content written for this session, not sourced from any real company or published case; it should not be presented as a real or licensed case study.
