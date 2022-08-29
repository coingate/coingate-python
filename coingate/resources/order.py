from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class BaseOrder(BaseModel):
    id: int
    status: str
    do_not_convert: bool
    price_currency: str
    price_amount: Decimal
    lightning_network: bool
    receive_currency: str
    receive_amount: str
    created_at: datetime
    order_id: str
    payment_url: str
    underpaid_amount: Decimal
    overpaid_amount: Decimal
    is_refundable: bool


class NewOrder(BaseOrder):
    token: str


class CheckoutPlatform(BaseModel):
    id: int
    title: str
    id_name: str


class Checkout(BaseOrder):
    pay_currency: str
    pay_amount: Decimal
    expire_at: datetime
    payment_address: str
    platform: CheckoutPlatform


class Order(BaseOrder):
    orderable_type: str
    orderable_id: int
    payment_address: str


class PaginatedOrders(BaseModel):
    current_page: int
    per_page: int
    total_order: int
    total_pages: int
    orders: list[Order]