from datetime import datetime
from decimal import Decimal
from typing import List

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


class PaginatedWithdrawalPayoutSetting(BaseModel):
    id: int
    title: str
    account_holder_name: str
    routing_number: str
    bank_name: str
    bank_address: str
    bank_city: str
    bank_country: str
    swift: str
    iban: str


class PaginatedWithdrawal(BaseModel):
    id: int
    status: str
    amount: Decimal
    created_at: datetime
    currency: Currency
    payout_setting: PaginatedWithdrawalPayoutSetting


class PaginatedWithdrawals(BaseModel):
    current_page: int
    per_page: int
    total_withdrawals: int
    total_pages: int
    withdrawals: List[PaginatedWithdrawal]
