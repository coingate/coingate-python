from decimal import Decimal
from typing import List

from pydantic import BaseModel


class LedgerAccountCurrency(BaseModel):
    id: int
    title: str
    symbol: str


class LedgerAccount(BaseModel):
    id: str
    balance: Decimal
    status: str
    currency: LedgerAccountCurrency


class PaginatedLedgerAccounts(BaseModel):
    current_page: int
    per_page: int
    total_accounts: int
    total_pages: int
    accounts: List[LedgerAccount]
