from dataclasses import dataclass

@dataclass
class Position:

    BUY = "BUY"
    SELL = "SELL"

    epic: str
    expiry: str
    direction: str
    size: float
    bid: float = None # Adding this for calc purposes, not an actual attribute in ig
    level: float = None
    orderType: str = "LIMIT"
    guaranteedStop: str = "false"
    forceOpen: str = "true"
    currencyCode: str = "USD"
    is_open: bool = False

    # Json from get positions has position and market attributes
    @classmethod
    def from_json_get_position_market(cls, json, is_open):

        return Position(
            epic=json['market']['epic'],
            expiry=json['market']['expiry'],
            direction=json['position']['direction'],
            size=float(json['position']['size']),
            level=json['position']['level'] if 'level' in json['position'] else None,
            currencyCode=json['position']['currency'],
            is_open=is_open,
            bid=json['market']['bid'] if 'bid' in json['market'] else None
        )

    @classmethod
    def create_open_order(cls, epic: str, expiry: str, size: str, level: float):
        return Position(epic, expiry, cls.BUY, size, level=level)

    def get_opening_details(self):
        return {
            "epic": self.epic,
            "expiry": self.expiry,
            "direction": self.direction,
            "size": self.size,
            "orderType": self.orderType,
            "level": self.level,
            "guaranteedStop": self.guaranteedStop,
            "forceOpen": self.forceOpen,
            "currencyCode": self.currencyCode
        }

    def get_closing_details(self, level):
        if self.direction == self.BUY:
            self.direction = self.SELL
        else:
            self.direction = self.BUY

        self.level = level

        return {
                "epic": self.epic,
                "expiry": self.expiry,
                "direction": self.direction,
                "size": self.size,
                "orderType": "LIMIT",
                "level": self.level
        }

    def get_base_details(self):
        return {
            "epic": self.epic,
            "expiry": self.expiry,
            "direction": self.direction,
            "size": self.size,
            "currencyCode": self.currencyCode,
            "isOpen": self.is_open,
            "level": self.level if self.level is not None else 0
        }

    # TODO add deal reference to this or something, this isn't good enough
    def __eq__(self, other) -> bool:
        if (
            self.epic == other.epic and 
            self.expiry == other.expiry and 
            self.direction == other.direction and 
            self.size == other.size
        ):
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)



@dataclass
class Market:

    instrumentName: str
    expiry: str
    epic: str
    instrumentType: str
    lotSize: float
    high: float
    low: float
    percentageChange: float
    netChange: float
    bid: float
    offer: float
    updateTime: str # Should really convert this to datetime
    updateTimeUTC: str # Should really convert this to datetime
    delayTime: float
    streamingPricesAvailable: str # Should really convert this to bool
    marketStatus: str 
    scalingFactor: int
