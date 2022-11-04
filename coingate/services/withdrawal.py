from typing import TYPE_CHECKING, Optional

from ..resources.withdrawal import PaginatedWithdrawals, Withdrawal

if TYPE_CHECKING:
    from ..client import CoinGate


class WithdrawalService:
    def __init__(self, client: "CoinGate"):
        self._client = client

    def get(self, id: str) -> Withdrawal:
        """Retrieves a specific withdrawal.

        :param int `id`: ID of withdrawal

        :rtype `:class:`<coingate.resources.withdrawal.Withdrawal>`

        Basic Usage::
          >>> client = CoinGate('YOUR_API_KEY')
          >>> client.withdrawal.get(1)

        """
        response = self._client.request("get", f"v2/withdrawals/{id}").json()
        return Withdrawal(**response)

    def get_all(self) -> PaginatedWithdrawals:
        """Retrieves all withdrawals.

        :rtype `:class:`<coingate.resources.withdrawal.PaginatedWithdrawals>`

        Basic Usage::
          >>> client = CoinGate('YOUR_API_KEY')
          >>> client.withdrawal.get_all()

        """
        response = self._client.request("get", "v2/withdrawals").json()
        return PaginatedWithdrawals(**response)
