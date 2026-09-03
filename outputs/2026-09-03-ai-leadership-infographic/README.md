# "Your Next AI Pilot Is Already Running a Leadership Test" — one-page infographic

- **Source material converted from:** Donham's final, verbatim instructional
  copy block (headline, subhead, four key points, boxed action takeaway, and
  NBER source line — all specified as final by Donham, not paraphrased by
  Copeland), itself synthesizing Weidmann, Xu & Deming (2025), *Measuring
  Human Leadership Skills with AI Agents*, NBER Working Paper No. 33662
  (Doriot's research find this session).
- **Target format:** single-page, portrait, HBS-branded executive infographic
  (crimson #A51C30 / black / charcoal #3A3A3A / white only).
- **Director / tools:** Copeland (Content Conversion & Production), via the
  **Canva connector** — confirmed live via `ListConnectors` before use
  (`connected: true`, `enabledInChat: true`). No brand kit existed to attach
  (`list-brand-kits` returned zero kits), so HBS colors were specified
  directly in the generation brief and then hand-corrected in the editor.
  Reasoning throughout on Claude Sonnet 5, included in Kaitlyn's existing
  Claude subscription — no separate API charge.
- **Real Canva design:**
  - Design ID: **`DAHUL405Jsg`**
  - Edit link: https://www.canva.com/d/FKG_AhXQWEqE2Ne
  - View link: https://www.canva.com/d/hvY2XBuVXhgXwOK
  - 1 page, 800×2000 (portrait), committed and saved in Canva.
- **QA pass — what actually happened, not just what was requested:**
  1. `generate-design` (design_type `infographic`) was called with the full
     verbatim copy and the HBS palette spelled out in detail. **What
     rendered did not match what was requested.** Canva's AI rewrote the
     headline, subhead, and all four points into generic marketing copy
     ("AI Leadership" / "Transform your leadership strategy today!" /
     three single-line labels: Predictive, Behavioral, Inclusive), dropped
     the boxed CTA's actual text, dropped the fourth point entirely, and
     dropped the NBER source line completely. The `verbatim` flag on the
     underlying tool only applies to `design_type: "doc"`, not
     `infographic` — there is no verbatim mode for this design type.
  2. Rather than ship that mismatch, the design was converted to a real
     editable Canva design (`create-design-from-candidate`) and then
     hand-corrected element-by-element via `read-design`/`edit-design`
     (opened a real editing transaction, replaced text node-by-node,
     resized/repositioned the CTA band, added the missing CTA label and
     source-line text nodes, fixed contrast on two new nodes that
     initially rendered black-on-crimson) until the on-canvas text matched
     Donham's copy verbatim. This was verified by re-reading the committed
     design content, not assumed from the edit calls succeeding.
  3. **Still a known, flagged gap:** the three supporting photographs
     (business leader, meeting, group of people) are Canva's own AI-picked
     stock imagery and contain natural skin tones / clothing colors outside
     the crimson/black/white/charcoal palette. The requested design type
     (`infographic`) does not offer a photography-free variant, and no
     brand kit existed to lock the palette at generation time. This is a
     genuine, unresolved deviation from the "no other hues anywhere" brand
     instruction — flagging it rather than claiming full compliance.
  4. **Environment limitation, also flagged rather than worked around:**
     `export-design` was called successfully and returned real, working
     PDF and PNG download URLs from Canva
     (`export-download.canva.com`, job IDs `e4d99bb9-3437-4726-91d0-50bcaea2263c`
     PDF and `8d604298-4187-48ee-80f0-b13b32ad2d36` PNG). This session's
     network egress proxy blocks that host (`connect_rejected` / HTTP 403,
     "organization policy"), so the rendered binary could **not** be pulled
     into this repo in this session — hence no `.pdf`/`.png` file sits
     alongside this README. The design itself is real and live at the
     Canva links above; anyone with edit access (or a session whose egress
     isn't blocked) can re-run `export-design` on `DAHUL405Jsg` and drop
     the file in this folder. The presigned export URLs generated this
     session expire within ~24 hours of generation (2026-09-03) and should
     be treated as already stale by the time anyone reads this.
  5. Not yet cleared: the `pedagogical_review` HITL checkpoint (Donham's
     instructional framing hasn't been re-reviewed against the final visual
     execution) and `external_publish` (nothing here is cleared for
     external/client-facing use yet).
- **Version:** 1 (verbatim-corrected draft, unreviewed, photography-palette
  gap open, binary export not yet committed to this repo).
- **Known open items:**
  1. Pull the actual PDF/PNG bytes into this folder from a session with
     unblocked egress (or have Kaitlyn export directly from the Canva edit
     link) and re-commit.
  2. Either replace the three stock photos with monochrome/duotone crimson
     treatments (achievable in the Canva editor: recolor or apply a
     crimson duotone filter to each circular image) or remove them if strict
     palette compliance is required before external use.
  3. Route through `pedagogical_review` and, if this is meant for anyone
     outside the workforce, `external_publish` before distribution.
