from decimal import Decimal

from coingate import CoinGate


class BaseTestCase:
    def setup_method(self):
        self.existing_big_order_id = (
            34058  # This is hardcoded because we cant mark as paid in API
        )
        self.client = CoinGate(
            api_key="HyW6QxVxFuFyfYNsTsmQftScWC2WYHUrSzCiqRX3", use_sanbox_mode=True
        )

    def _create_test_order(
        self,
        price_amount: Decimal = Decimal("10"),
        price_currency: str = "EUR",
        receive_currency: str = "EUR",
        **kwargs
    ):
        return self.client.order.create(
            price_amount, price_currency, receive_currency, **kwargs
        )
