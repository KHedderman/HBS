"""Outbound sync adapters: GitHub, Notion, Airtable.

Every function here degrades gracefully to a no-op + log line when its
credentials aren't configured, so the rest of the system (routing, memory,
HITL) is fully testable without any external accounts.
"""
