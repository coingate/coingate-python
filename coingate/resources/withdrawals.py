from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from .platform import Platform
from .public import Currency


class PayoutSetting(BaseModel):
    id: int
    title: str
    address: str
    currency: Currency


class Withdrawal(BaseModel):
    id: int
    status: str
    amount: Decimal
    created_at: datetime
    completed_at: datetime
    currency: Currency
    payout_setting: PayoutSetting
    platform: Platform
