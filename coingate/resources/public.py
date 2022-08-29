from datetime import datetime
from decimal import Decimal
from typing import NewType, Optional

from pydantic import BaseModel

NestedCurrencyObject = NewType(
    "NestedCurrencyObject", dict[str, dict[str, Optional[Decimal]]]
)


class ExchangeTrader(BaseModel):
    buy: NestedCurrencyObject
    sell: NestedCurrencyObject


class ExchangesRates(BaseModel):
    merchant: NestedCurrencyObject
    trader: ExchangeTrader


class Ping(BaseModel):
    ping: str
    time: datetime


class CurrencyMerchant(BaseModel):
    price: bool
    pay: bool
    receive: bool


class CurrencyPlatform(BaseModel):
    id: int
    id_name: str
    title: str
    enabled: bool


class Currency(BaseModel):
    id: int
    title: str
    kind: str
    symbol: str
    native: bool
    disabled: bool
    disabled_message: Optional[str]
    merchant: Optional[CurrencyMerchant]
    platforms: Optional[list[CurrencyPlatform]]


class PlatformCurrency(BaseModel):
    id: int
    title: str
    symbol: str
    enabled: bool


class Platform(BaseModel):
    id: int
    title: str
    id_name: str
    disabled: bool
    disabled_message: Optional[str]
    currencies: list[PlatformCurrency]
