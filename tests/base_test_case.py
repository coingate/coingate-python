from coingate import CoinGate


class BaseTestCase:
    def setup_method(self):
        self.client = CoinGate(use_sanbox_mode=True)
