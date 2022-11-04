from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from ..resources.refund import PaginatedRefunds, Refund

if TYPE_CHECKING:
    from ..client import CoinGate


class RefundService:
    def __init__(self, client: "CoinGate"):
        self._client = client

    def create_order_refund(
        self,
        order_id: int,
        amount: Decimal,
        address: str,
        currency_id: int,
        platform_id: int,
        reason: str,
        email: str,
        ledger_account_id: str,
        *,
        address_memo: Optional[str] = None,
    ) -> Refund:
        """Creates a refund for an order.

        :param int `order_id`: ID of the order to be refunded
        :param Decimal `amount`: Requesting amount in order price currency to refund
        :param str `address`: Cryptocurrency address to which the refund will be sent
        :param Optional[str] `address_memo`
        :param int `currency_id`: ID of the currency in which the refund will be issued
        :param int `platform_id`: Platform ID of the currency in which the refund will be issued
        :param str `reason`: Reason for issuing the refund
        :param str `email`: Customer will receive updates on refund status to this email
        :param str `ledger_account_id`: ID of the trader balance associated with the currency in which the refund will be issued

        :rtype `:class:`<coingate.resources.refund.Refund>`

        Basic Usage::
          >>> client = CoinGate('YOUR_API_KEY')
          >>> client.refund.create_order_refund(1, Decimal('10'), 'addy', 1, 1, 'refund', 'email@email.com', 'id')

        """
        res = self._client.request(
            "post",
            f"v2/orders/{order_id}/refunds",
            data={
                "amount": amount,
                "address": address,
                "address_memo": address_memo,
                "currency_id": currency_id,
                "platform_id": platform_id,
                "reason": reason,
                "email": email,
                "ledger_account_id": ledger_account_id,
            },
        ).json()

        return Refund(**res)

    def get_order_refund(self, order_id: int, id: int) -> Refund:
        """Retrieves a specific refund for an order.

        :param int `order_id`: ID of the order to be refunded
        :param int `id`: ID of the refund

        :rtype `:class:`<coingate.resources.refund.Refund>`

        Basic Usage::
          >>> client = CoinGate('YOUR_API_KEY')
          >>> client.refund.get_order_refund(1, 1)

        """
        res = self._client.request("get", f"v2/orders/{order_id}/refunds/{id}").json()
        return Refund(**res)

    def get_order_refunds(
        self, order_id: int, *, page: Optional[int] = 1, per_page: Optional[int] = 100
    ) -> PaginatedRefunds:
        """Retrieves all refunds for an order.

        :param int `order_id`: ID of the order to be refunded
        :param Optional[int] `page`: Current page number
        :param Optional[int] `per_page`: Number of refunds per page

        :rtype `:class:`<coingate.resources.refund.PaginatedRefunds>`

        Basic Usage::
          >>> client = CoinGate('YOUR_API_KEY')
          >>> client.refund.get_order_refunds(1)

        """
        res = self._client.request(
            "get",
            f"v2/orders/{order_id}/refunds",
            data={
                "page": page,
                "per_page": per_page,
            },
        ).json()

        return PaginatedRefunds(**res)

    def get_refunds(self, *, page: int = 1, per_page: int = 100) -> PaginatedRefunds:
        """Retrieves all refunds.

        :param Optional[int] `page`: Current page number
        :param Optional[int] `per_page`: Number of refunds per page

        :rtype `:class:`<coingate.resources.refund.PaginatedRefunds>`

        Basic Usage::
          >>> client = CoinGate('YOUR_API_KEY')
          >>> client.refund.get_refunds()

        """
        res = self._client.request(
            "get",
            "v2/refunds",
            data={"page": page, "per_page": per_page},
        ).json()

        return PaginatedRefunds(**res)
