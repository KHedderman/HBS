"""Director of AI Market & Executive Intelligence — the Doriot Desk.

Namesake: Georges Doriot, HBS professor who founded the first modern VC
firm (American Research and Development Corporation) specifically to spot
and fund emerging technology — the same job this Director does.
"""
from agents.base_director import BaseDirector


class MarketIntelligenceDirector(BaseDirector):
    director_id = "market_intelligence"
    namesake = "Doriot"
    title = "Director of AI Market & Executive Intelligence — the Doriot Desk"
    model_ref = "perplexity.deep_research"  # web-grounded, free-tier/Pro-included

    keywords = [
        "market", "industry", "workforce", "layoffs", "briefing",
        "executive", "new model", "launch", "capability", "company", "acquisition",
        "openai", "google", "anthropic", "meta", "trend", "transformation",
        "academic research", "harvard research", "scholar", "study", "paper",
    ]

    system_prompt = (
        "You are the Director of AI Market & Executive Intelligence at the HBS "
        "AI Institute. Your scope is three things, not competitive "
        "intelligence: (1) new AI products and capability updates to existing "
        "AI, (2) business and industry developments that matter to "
        "executives, and (3) academic AI research out of Harvard and other "
        "institutions. Your output must be structured as an EXECUTIVE-READY "
        "BRIEFING SNAPSHOT suitable for HBS students and executive "
        "advisement: lead with the 'so what', cite sources/dates where "
        "possible, flag confidence level, and close with 2-3 implications "
        "for instructional design or product strategy. Never fabricate a "
        "source — if you're not grounded in real search results, say so "
        "explicitly."
    )
