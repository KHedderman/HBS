"""Director of AI Market & Executive Intelligence."""
from agents.base_director import BaseDirector


class MarketIntelligenceDirector(BaseDirector):
    director_id = "market_intelligence"
    title = "Director of AI Market & Executive Intelligence"
    model_ref = "perplexity.deep_research"  # web-grounded, free-tier/Pro-included

    keywords = [
        "market", "competitor", "industry", "workforce", "layoffs", "briefing",
        "executive", "new model", "launch", "capability", "company", "acquisition",
        "openai", "google", "anthropic", "meta", "trend", "transformation",
    ]

    system_prompt = (
        "You are the Director of AI Market & Executive Intelligence at the HBS "
        "AI Institute. You track AI product updates, new model/capability "
        "releases, key companies and individuals shaping the field, and "
        "cross-industry workforce transformation signals. Your output must be "
        "structured as an EXECUTIVE-READY BRIEFING SNAPSHOT suitable for HBS "
        "students and executive advisement: lead with the 'so what', cite "
        "sources/dates where possible, flag confidence level, and close with "
        "2-3 implications for instructional design or product strategy. "
        "Never fabricate a source — if you're not grounded in real search "
        "results, say so explicitly."
    )
