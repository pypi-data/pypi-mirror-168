from dataclasses import dataclass
from typing import *

@dataclass
class Transaction:
    cashTransaction: bool = None
    closeLevel: str = None
    currency: str = None
    date: str = None
    dateUtc: str = None
    instrumentName: str = None
    openDateUtc: str = None
    openLevel: str = None
    period: str = None
    profitAndLoss: str = None
    reference: str = None
    size: str = None
    transactionType: str = None