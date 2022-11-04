from decimal import Decimal
from typing import List

from pydantic import BaseModel

from .currency import Currency


class LedgerAccount(BaseModel):
    id: str
    balance: Decimal
    status: str
    currency: Currency


class PaginatedLedgerAccounts(BaseModel):
    current_page: int
    per_page: int
    total_accounts: int
    total_pages: int
    accounts: List[LedgerAccount]
