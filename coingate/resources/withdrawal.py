from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from .platform import Platform
from .public import Currency


class Withdrawal(BaseModel):
    id: int
    status: str
    amount: Decimal
    created_at: datetime
    completed_at: Optional[datetime]
    currency: Currency
    payout_setting: Dict[str, Any]
    platform: Optional[Platform]


class PaginatedWithdrawals(BaseModel):
    current_page: int
    per_page: int
    total_withdrawals: int
    total_pages: int
    withdrawals: List[Withdrawal]
