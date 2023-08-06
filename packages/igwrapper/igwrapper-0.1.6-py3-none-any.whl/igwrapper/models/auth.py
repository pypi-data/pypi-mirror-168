from dataclasses import dataclass
from typing import *

from accounts import *
from enums import *

@dataclass
class AuthV2:
    accountInfo: AccountInfo = None
    accountType: AccountType = None
    accounts: List[Account] = None
    clientId: str = None
    currencyIsoCode: str = None
    currencySymbol: str = None
    currentAccountId: str = None
    dealingEnabled: bool = None
    hasActiveDemoAccounts: bool = None
    hasActiveLiveAccounts: bool = None
    lightstreamerEndpoint: str = None
    reroutingEnvironment: ReroutingEnvironment = None
    timezoneOffset: float = None
    trailingStopsEnabled: bool = None
    cst: str = None
    x_security_token: str = None
