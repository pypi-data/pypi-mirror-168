from dataclasses import dataclass
from typing import *

@dataclass
class Price:
    ask: float = None
    bid: float = None

@dataclass
class MarketPrice:
    closePrice: Price = None
    highPrice: Price = None
    lowPrice: Price = None
    openPrice: Price = None
    lastTradedVolume: float = None
    snapshotTime: str = None
    snapshotTimeUTC: str = None