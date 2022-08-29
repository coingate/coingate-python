from coingate import CoinGate


class BaseTestCase:
    def setup_method(self):
        self.client = CoinGate(api_key="HyW6QxVxFuFyfYNsTsmQftScWC2WYHUrSzCiqRX3", use_sanbox_mode=True)
