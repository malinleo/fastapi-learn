import faust


class CollectSecurityOverview(faust.Record):
    """Security overview record."""
    symbol: str
    exchange: str
