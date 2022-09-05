from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel


class RefundOrder(BaseModel):
    id: int


class RefundCurrencyPlatform(BaseModel):
    id: int
    title: str


class RefundCurrency(BaseModel):
    id: int
    title: str
    symbol: str
    platform: RefundCurrencyPlatform


class RefundLedgerAccountCurrency(BaseModel):
    id: int
    title: str
    symbol: str


class RefundLedgerAccount(BaseModel):
    id: str
    currency: RefundLedgerAccountCurrency


class Refund(BaseModel):
    id: int
    request_amount: Decimal
    refund_amount: Decimal
    address: str
    status: str
    memo: Optional[str]
    created_at: datetime
    order: RefundOrder
    refund_currency: RefundCurrency
    transactions: List
    ledger_account: RefundLedgerAccount


class PaginatedRefundsRefund(BaseModel):
    id: int
    request_amount: Decimal
    refund_amount: Decimal
    crypto_address: Optional[str]
    crypto_address_memo: Optional[str]
    status: str
    order: RefundOrder
    refund_currency: RefundCurrency


class PaginatedRefunds(BaseModel):
    current_page: int
    per_page: int
    total_refunds: int
    total_pages: int
    refunds: List[PaginatedRefundsRefund]
