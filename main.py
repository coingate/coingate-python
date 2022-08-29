from decimal import Decimal

from coingate import CoinGate

if __name__ == "__main__":
    c = CoinGate(
        api_key="HyW6QxVxFuFyfYNsTsmQftScWC2WYHUrSzCiqRX3", use_sanbox_mode=True
    )

    order = c.order.create(Decimal("10"), "EUR", "DO_NOT_CONVERT")

    print(order)
