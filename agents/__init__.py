"""HBS AI Institute Multi-Agent Content Command Center — agents package.

Hub-and-spoke architecture:
    ChiefOfStaff (hub, Intelligent Router)
        -> dispatches in parallel to Director subclasses (spokes)
        -> Directors never talk to each other
        -> Director outputs return only to ChiefOfStaff for synthesis
    MemoryCurator runs alongside the hub as the persistent context engine.
"""
