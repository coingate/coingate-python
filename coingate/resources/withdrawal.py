from datetime import datetime
from decimal import Decimal
from typing import List, Optional

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
    completed_at: Optional[datetime]
    currency: Currency
    payout_setting: PayoutSetting
    platform: Optional[Platform]


class PaginatedWithdrawals(BaseModel):
    current_page: int
    per_page: int
    total_withdrawals: int
    total_pages: int
    withdrawals: List[Withdrawal]
