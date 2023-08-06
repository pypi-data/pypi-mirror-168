from dataclasses import dataclass
from typing import *

from enums import *

@dataclass
class Action:

    actionType: DealActionType = None
    affectedDealId: str = None

@dataclass
class Details:

    actions: List[Action] = None
    currency: str = None
    dealReference: str = None
    direction: DealDirection = None
    goodTillDate: str = None
    guaranteedStop: bool = None
    level: float = None
    limitDistance: float = None
    limitLevel: float = None
    marketName: str = None
    size: float = None
    stopDistance: float = None
    stopLevel: float = None
    trailingStep: float = None
    trailingStopDistance: float = None


@dataclass
class Activity:

    channel: HistoryActivityChannel = None
    date: str = None
    dealId: str = None
    description: str = None
    details: Details = None
    epic: str = None
    period: str = None
    status: ActivityStatus = None
    type: ActivityType = None
