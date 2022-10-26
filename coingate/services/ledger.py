from typing import TYPE_CHECKING, Optional

from ..resources.ledger import LedgerAccount, PaginatedLedgerAccounts

if TYPE_CHECKING:
    from ..client import CoinGate


class LedgerService:
    def __init__(self, client: "CoinGate"):
        self._client = client

    def get(self, id: str) -> LedgerAccount:
        """Retrieves a specific ledger account.

        :param str `id`: ID of ledger account

        :rtype `:class:`<coingate.resources.ledger.LedgerAccount>`

        Basic Usage::
          >>> client = CoinGate('YOUR_API_KEY')
          >>> client.ledger.get('ledger_id')

        """
        response = self._client.request("get", f"v2/ledger/accounts/{id}").json()
        return LedgerAccount(**response)

    def get_all(
        self, *, page: Optional[int] = None, per_page: Optional[int] = None
    ) -> PaginatedLedgerAccounts:
        """Retrieves all ledger accounts.

        :param Optional[int] `page`: Current page number. Default: 1
        :param Optional[int] `per_page`: Number of accounts per page. Max: 100. Default: 100

        :rtype `:class:`<coingate.resources.ledger.PaginatedLedgerAccounts>`

        Basic Usage::
          >>> client = CoinGate('YOUR_API_KEY')
          >>> client.ledger.get_all()

        """
        response = self._client.request(
            "get", "v2/ledger/accounts", data={"page": page, "per_page": per_page}
        ).json()

        return PaginatedLedgerAccounts(**response)
