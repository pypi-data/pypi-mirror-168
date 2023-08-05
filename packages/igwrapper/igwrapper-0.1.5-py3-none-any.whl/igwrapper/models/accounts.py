from dataclasses import dataclass

from enums import *

@dataclass
class AccountBalance:

    available: float = None
    balance: float = None
    deposit: float = None
    profitLoss: float = None

@dataclass
class Account:

    accountAlias: str = None
    accountId: str = None
    accountName: str = None
    accountType: AccountType = None
    balance: AccountBalance = None
    canTransferFrom: bool = None
    canTransferTo: bool = None
    currency: str = None
    preferred: bool = None
    status: AccountStatus = None

@dataclass
class AccountInfo:

    available: float = None
    balance: float = None
    deposit: float = None
    profitLoss: float = None