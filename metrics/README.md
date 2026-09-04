# Learning metrics

`learning_metrics.jsonl` is Henderson's real, in-repo instrument — one
JSON object per line, one line per data point collected about a session,
module, or program. This exists so Henderson has an actual store to read
and report on instead of a system prompt with nothing behind it (a real
gap flagged 2026-09-03).

## Schema

```json
{"timestamp": "ISO-8601", "program": "string", "metric": "string", "value": "number or string", "source": "string", "notes": "string (optional)"}
```

## The 5 draft metrics

These are Kaitlyn's placeholder starting set, chosen because they're
standard for executive-education programs and each maps to a concrete,
collectible number — **not** confirmed HBS AI Institute measures. Public
research couldn't establish what the Institute specifically tracks, so
treat this as a draft to verify with the hiring manager, not something to
present as settled in the interview.

| metric | what it captures | typical source |
|---|---|---|
| `session_satisfaction` | Post-session participant rating (e.g. 1-5 or NPS-style) | Post-session survey |
| `knowledge_delta` | Pre/post self-assessed or tested competency change | Pre/post check-in |
| `completion_rate` | % of enrolled participants completing the program/module | Program roster |
| `facilitator_engagement_rating` | Facilitator's own rating of participant engagement during the session | Facilitator debrief |
| `time_to_competency` | Time from program start to a defined competency milestone | Program tracking |

## How an entry gets added

Until a real survey/analytics connector is chosen and connected:

```bash
python scripts/eliot_log_metric.py \
    --program "Deciding Where to Deploy AI in Your Function" \
    --metric session_satisfaction \
    --value 4.6 \
    --source "Post-session survey" \
    --notes "n=18 VPs, first live run"
```

This validates the entry against `agents.schemas.MetricEntry` before
appending, so a malformed line fails at write time instead of silently
corrupting the one instrument Henderson reads from. Each entry should be
real data from an actual session or program, not a placeholder; an empty
file is honest (no programs run yet), a file full of invented numbers is
not.
