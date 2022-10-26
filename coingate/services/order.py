from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from ..resources.order import Checkout, NewOrder, Order, PaginatedOrders
from ..utils import date_to_str_or_none

if TYPE_CHECKING:
    from ..client import CoinGate


class OrderService:
    def __init__(self, client: "CoinGate"):
        self._client = client

    def create(
        self,
        price_amount: Decimal,
        price_currency: str,
        receive_currency: str,
        *,
        order_id: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        callback_url: Optional[str] = None,
        cancel_url: Optional[str] = None,
        success_url: Optional[str] = None,
        token: Optional[str] = None,
        purchaser_email: Optional[str] = None,
    ) -> NewOrder:
        """Create order at CoinGate and redirect shopper to invoice (payment_url).

        :param Optional[str] `order_id`: Merchant's custom order ID. We recommend using a unique order ID
        :param Decimal `price_amount`: The price set by the merchant
        :param str `price_currency`: ISO 4217 currency code which defines the currency in which you wish to price your merchandise; used to define price parameter.
        :param str `receive_currency`: ISO 4217 currency code which defines the currency in which you wish to receive your settlements. Currency conversions are done by CoinGate. Possible values: fiat - EUR; stablecoin - USDT; crypto: BTC, LTC, ETH or DO_NOT_CONVERT. Note: use DO_NOT_CONVERT to keep payments received in original currency (Altcoin payments will be converted to BTC). With DO_NOT_CONVERT you can also extend invoice expiration time up to 24 hours.
        :param Optional[str] `title`: Max 150 characters. Example: product title (Apple iPhone 14), order id (MyShop Order #12345), cart id
        :param Optional[str] `description`: More details about this order. Max 500 characters. It can be cart items, product details or other information. Example: 1 x Apple iPhone 14, 1 x Apple MacBook Air.
        :param Optional[str] `callback_url`: Send an automated message to Merchant URL when order status is changed.
        :param Optional[str] `cancel_url`: Redirect to Merchant URL when buyer cancels the order
        :param Optional[str] `success_url`: Redirect to Merchant URL after successful payment
        :param Optional[str] `token`: Your custom token to validate payment callback (notification)
        :param Optional[str] `purchaser_email`: Email address of the purchaser (payee) provided will be pre-filled on the invoice.

        :rtype `:class`<coingate.resources.order.NewOrder>`

        Basic Usage::
          >>> client = CoinGate('YOUR_API_KEY')
          >>> client.order.create(Decimal('10'), 'EUR', 'EUR')

        """
        response = self._client.request(
            "post",
            "v2/orders",
            data={
                "order_id": order_id,
                "price_amount": price_amount,
                "price_currency": price_currency,
                "receive_currency": receive_currency,
                "title": title,
                "description": description,
                "callback_url": callback_url,
                "cancel_url": cancel_url,
                "success_url": success_url,
                "token": token,
                "purchaser_email": purchaser_email,
            },
        ).json()

        return NewOrder(**response)

    def checkout(
        self,
        id: int,
        pay_currency: str,
        *,
        lightning_network: Optional[bool] = None,
        purchaser_email: Optional[str] = None,
        platform_id: Optional[int] = None,
    ) -> Checkout:
        """Placing created order with pre-selected payment currency (BTC, LTC, ETH, etc). Display payment_address and pay_amount for shopper or redirect to payment_url. Can be used to white-label invoices

        :param int `id`: CoinGate order ID
        :param str `pay_currency`: Payment cryptocurrency. Possible values: BTC, LTC, etc. Other cryptocurrencies are processed via a third party and are not accessible with the Checkout method
        :param Optional[bool] `lightning_network`: Lightning network parameter is optional and it is available only for BTC and LTC cryptocurrencies. Maximum available price amount for lightning network orders is 0.042 BTC equivalent
        :param Optional[str] `purchaser_email`: Email address of the purchaser (payee) provided will be pre-filled on the invoice
        :param Optional[int] `platform_id`: Is an optional parameter where you can select on what blockchain (platform) the particular digital asset is expected to be received. By default (if the parameter is empty) the system will generate the invoice on the NATIVE blockchain (Binance chain for BNB, Bitcoin chain for BTC, Ethereum chain for ETH, etc.) or on Ethereum blockchain for Tokens (BUSD, DAI USDT, etc.)

        :rtype `:class:`<coingate.resources.order.Checkout>`

        Basic Usage::
          >>> client = CoinGate('YOUR_API_KEY')
          >>> client.order.checkout(123, 'EUR')

        """
        response = self._client.request(
            "post",
            f"v2/orders/{id}/checkout",
            data={
                "pay_currency": pay_currency,
                "lightning_network": lightning_network,
                "purchaser_email": purchaser_email,
                "platform_id": platform_id,
            },
        ).json()

        return Checkout(**response)

    def get(self, id: int) -> Order:
        """Before making a GET order request, a user should have an already CREATED order, which can be paid or canceled.
        After creating an order, you will get an ORDER ID. This ID will be used for GET ORDER requests.

        :param int `id`: CoinGate Order id

        :rtype `:class:`<coingate.resources.order.Order>`

        Basic Usage::
          >>> client = CoinGate('YOUR_API_KEY')
          >>> client.order.get(123)

        """
        response = self._client.request("get", f"v2/orders/{id}").json()
        return Order(**response)

    def get_all(
        self,
        *,
        per_page: Optional[int] = None,
        page: Optional[int] = None,
        sort: Optional[str] = None,
        created_from: Optional[datetime] = None,
        created_to: Optional[datetime] = None,
    ) -> PaginatedOrders:
        """Retrieving information of all placed orders.

        :param Optional[int] `per_page`: How many orders per page. Max: 100. Default: 100
        :param Optional[int] `page`: Default: 1
        :param Optional[str] `sort`: Sort orders by field. Available sort options: created_at_asc, created_at_desc. Default: created_at_desc
        :param Optional[str] `created_from`: Where order creation time is equal or greater
        :param Optional[str] `created_to`: Where order creation time is equal or greater

        :rtype `:class:`<coingate.resources.order.PaginatedOrders>`

        Basic Usage::
          >>> client = CoinGate('YOUR_API_KEY')
          >>> client.order.get_all()

        """
        response = self._client.request(
            "get",
            "v2/orders",
            params={
                "per_page": per_page,
                "page": page,
                "sort": sort,
                "created_at[from]": date_to_str_or_none(created_from),
                "created_at[to]": date_to_str_or_none(created_to),
            },
        ).json()

        return PaginatedOrders(**response)
