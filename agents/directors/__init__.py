"""Specialized Directors (spokes).

Every Director subclasses BaseDirector and is registered in
`agents.directors.REGISTRY` for the Chief of Staff's router to dispatch to.
Directors never import each other — all cross-domain work is synthesized by
the Chief of Staff after outputs return to the hub.
"""
from agents.directors.market_intelligence import MarketIntelligenceDirector
from agents.directors.pedagogical_synthesis import PedagogicalSynthesisDirector
from agents.directors.product_management import ProductManagementDirector
from agents.directors.project_management import ProjectManagementDirector
from agents.directors.ui_ux_architecture import UIUXArchitectureDirector
from agents.directors.growth_content import GrowthContentDirector
from agents.directors.multimedia_production import MultimediaProductionDirector
from agents.directors.analytics_reporting import AnalyticsReportingDirector
from agents.directors.accessibility_compliance import AccessibilityComplianceDirector
from agents.directors.content_production import ContentProductionDirector

REGISTRY = {
    "market_intelligence": MarketIntelligenceDirector,
    "pedagogical_synthesis": PedagogicalSynthesisDirector,
    "product_management": ProductManagementDirector,
    "project_management": ProjectManagementDirector,
    "ui_ux_architecture": UIUXArchitectureDirector,
    "growth_content": GrowthContentDirector,
    "multimedia_production": MultimediaProductionDirector,
    "analytics_reporting": AnalyticsReportingDirector,
    "accessibility_compliance": AccessibilityComplianceDirector,
    "content_production": ContentProductionDirector,
}
