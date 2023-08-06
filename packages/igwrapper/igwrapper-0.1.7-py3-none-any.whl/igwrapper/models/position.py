from dataclasses import dataclass
from typing import *

try:
    from ..models.enums import *
except ImportError:
    from .enums import *


@dataclass
class Market:
        
    bid: float = None
    delayTime: float = None
    epic: str = None
    expiry: str = None
    high: float = None
    instrumentName: str = None
    instrumentType: InstrumentType = None
    lotSize: float = None
    low: float = None
    marketStatus: MarketStatus = None
    netChange: float = None
    offer: float = None
    percentageChange: float = None
    scalingFactor: float = None
    streamingPricesAvailable: bool = None
    updateTime: str = None
    updateTimeUTC: str = None

@dataclass
class Position:

    contractSize: float = None
    controlledRisk: bool = None
    createdDate: str = None
    createdDateUTC: str = None
    currency: str = None
    dealId: str = None
    dealReference: str = None
    direction: DealDirection = None
    level: float = None
    limitLevel: float = None
    limitedRiskPremium: float = None
    size: float = None
    stopLevel: float = None
    trailingStep: float = None
    trailingStopDistance: float = None

@dataclass
class Otc(Market, Position):

    currencyCode: str = "USD"
    forceOpen: bool = True
    guaranteedStop: bool = False
    limitDistance: float = None
    orderType: OrderType = OrderType.LIMIT
    quoteId: str = None
    timeInForce: TimeInForce = None
    trailingStop: bool = None
    trailingStopIncrement: float = None
