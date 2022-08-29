from datetime import datetime
from decimal import Decimal
from typing import List

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
    memo: str
    created_at: datetime
    order: RefundOrder
    refund_currency: RefundCurrency
    transactions: List
    ledger_account: RefundLedgerAccount


class PaginatedRefundsRefund(BaseModel):
    id: int
    request_amount: str
    refund_amount: str
    crypto_address: str
    crypto_address_memo: str
    status: str
    order: RefundOrder
    refund_currency: RefundCurrency


class PaginatedRefunds(BaseModel):
    current_page: int
    per_page: int
    total_refunds: int
    total_pages: int
    refunds: List[PaginatedRefundsRefund]
