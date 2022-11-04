from datetime import datetime
from decimal import Decimal
from typing import Dict, List, NewType, Optional

from pydantic import BaseModel

from .currency import Currency
from .platform import Platform

NestedCurrencyObject = NewType(
    "NestedCurrencyObject", Dict[str, Dict[str, Optional[Decimal]]]
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


class CurrencyPlatform(Platform):
    enabled: bool


class PublicCurrency(Currency):
    kind: str
    native: bool
    disabled: bool
    disabled_message: Optional[str]
    merchant: Optional[CurrencyMerchant]
    platforms: Optional[List[CurrencyPlatform]]


class PlatformCurrency(Currency):
    enabled: bool


class PublicPlatform(Platform):
    disabled: bool
    disabled_message: Optional[str]
    currencies: List[PlatformCurrency]
