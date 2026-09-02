# Memory Schema

The Memory Curator persists two parallel logs:

## `memory/session_logs/<YYYY-MM-DD>.jsonl`
Raw, append-only, one line per Chief-of-Staff exchange for that calendar day.
Never edited or deduplicated — this is the audit trail.

```json
{
  "timestamp": "2026-09-02T14:03:11Z",
  "request": "Draft an executive briefing on the latest agentic AI launches",
  "response": "<full synthesized Chief of Staff response>",
  "directors_invoked": ["market_intelligence"],
  "tags": []
}
```

## `memory/long_term/knowledge_base.jsonl`
The curated store `MemoryCurator.recall()` searches. Currently a 1:1 append
of every session-log record (dependency-free keyword recall). When you're
ready to move beyond keyword overlap, swap `recall()` in
`agents/memory_curator.py` for an embeddings-backed retriever — the schema
here already gives you clean `request` / `response` / `tags` fields to embed.

## Sync targets
Every curated entry is also pushed to:
- **GitHub** — `memory/long_term/knowledge_base.jsonl` is committed (and, with
  `GITHUB_TOKEN` set, pushed via the API) on every `remember()` call.
- **Notion** — a page is created in the database at `NOTION_MEMORY_DATABASE_ID`
  with the request as the title and the response as the body, tagged.

Both syncs degrade to a logged no-op when their credentials aren't configured
— see `database_sync/github_sync.py` and `database_sync/notion_sync.py`.
