# CoinGate Python SDK (API v2)

![StaticCheckAndTestCI](https://github.com/markkkkas/coingate-python/actions/workflows/static-check-tests.yml/badge.svg)

This SDK provides conveniet way to communicate between CoinGate API v2 and your Python code.

## Requirements
Python 3.9+

## Installing
```
pip install coingate-python
```

## Dependencies
This library requires the following packages to work properly:
- [requests](https://pypi.org/project/requests/)
- [pydantic](https://pypi.org/project/pydantic/)

## Getting started
You can sign up for a CoinGate account at https://coingate.com for production and https://sandbox.coingate.com for testing (sandbox).

Please note, that for Sandbox you must generate separate API credentials on https://sandbox.coingate.com. API credentials generated on https://coingate.com will not work for Sandbox mode.

Usage of SDK looks like:
```py
>>> from coingate import CoinGate
>>> client = CoinGate("YOUR_API_TOKEN")
```

In order, to use sandbox mode, you need to pass second parameter as `True`
```py
>>> from coingate import CoinGate
>>> client = CoinGate("YOUR_API_TOKEN", True)
```

If you planning to use only Public API endpoints, you can initialize client without parameters
```py
>>> from coingate import CoinGate
>>> client = CoinGate()
```

## Public API

### Get Exchange Rate
Current exchange rate for any two currencies, fiat or crypto. This endpoint is public, authentication is not required.

```py
# Get exchange rate for Merchants
>>> client.public.get_exchange_rate_for_merchant(from_currency="EUR", to_currency="BTC")
Decimal('0.0000472')

# Get exchange rate for Traders
>>> client.public.get_exchange_rate_for_trader(kind="buy", from_currency="EUR", to_currency="ETH")
Decimal('0.00063213')
```

### List Exchange Rates
Current CoinGate exchange rates for Merchants and Traders. This endpoint is public, authentication is not required.

```py
# Get all exchange rates for Merchants and Traders
>>> client.public.get_all_exchange_rates()
ExchangeRates(
    merchant={
        'BTC': {
            'EUR': Decimal('7449.99'),
            'USD': Decimal('9139.34'),
            'ETH': Decimal('13.18044023')
        },
        'EUR': {
            'BTC': '0.00013351',
            'USD': '1.2317',
            'ETH': '0.00175954'
        }
    }
    trader=ExchangeTrader(
        buy={
            'BTC': {
                'EUR': Decimal('7449.99'),
                'USD': Decimal('9139.34'),
                'ETH': Decimal('13.18044023')
            },
            'EUR': {
                'BTC': '0.00013351',
                'USD': '1.2317',
                'ETH': '0.00175954'
            }
        }
        sell={
            'BTC': {
                'EUR': Decimal('7449.99'),
                'USD': Decimal('9139.34'),
                'ETH': Decimal('13.18044023')
            },
            'EUR': {
                'BTC': '0.00013351',
                'USD': '1.2317',
                'ETH': '0.00175954'
            }
        }
    )
)

# Get all exchange rates for Merchants
>>> client.public.get_merchant_exchange_rates()
{
    'BTC': {
        'EUR': Decimal('7449.99'),
        'USD': Decimal('9139.34'),
        'ETH': Decimal('13.18044023')
    },
    'EUR': {
        'BTC': '0.00013351',
        'USD': '1.2317',
        'ETH': '0.00175954'
    }
}

# Get all exchange rates for Traders
>>> client.public.get_trader_exchange_rates()
ExchangeTrader(
    buy={
        'BTC': {
            'EUR': Decimal('7449.99'),
            'USD': Decimal('9139.34'),
            'ETH': Decimal('13.18044023')
        },
        'EUR': {
            'BTC': '0.00013351',
            'USD': '1.2317',
            'ETH': '0.00175954'
        }
    }
    sell={
        'BTC': {
            'EUR': Decimal('7449.99'),
            'USD': Decimal('9139.34'),
            'ETH': Decimal('13.18044023')
        },
        'EUR': {
            'BTC': '0.00013351',
            'USD': '1.2317',
            'ETH': '0.00175954'
        }
    }
)
```

### Ping
A health check endpoint for CoinGate API. This endpoint is public, authentication is not required.

```py
>>> client.public.ping()
Ping(ping='pong', time='2017-12-13T19:07:18+00:00')
```

### IP Addresses
Get IP addresses of CoinGate servers

```py
>>> client.public.get_ip_addresses(separator="|")
'52.28.22.118|35.156.68.160'
```

### Get Currencies
Retrieves all currencies.

```py
>>> client.public.get_currencies(native=True, enabled=True, merchant_pay=True, merchant_receive=True, kind="crypto")
[
    Currency(id=1,
        title='Bitcoin',
        kind='crypto',
        native=True,
        disabled=False,
        disabled_message=None,
        merchant=CurrencyMerchant(price=True, pay=True, receive=True),
        platforms=[
            CurrencyPlatform(id=8, id_name='bitcoin', title='Bitcoin' enabled=True)
        ]
    ),
    Currency(
        id=2,
        title='Euro',
        kind='fiat',
        symbol='EUR',
        native=True,
        disabled=False,
        disabled_message=None,
        merchant=CurrencyMerchant(price=True, pay=False, receive=True),
        platforms=None
    ),
    Currency(
        id=3,
        title='United States dollar',
        kind='fiat',
        symbol='USD',
        native=True,
        disabled=False,
        disabled_message=None,
        merchant=CurrencyMerchant(price=True, pay=False, receive=True),
        platforms=None
    ),
    Currency(
        id=4,
        title='British Pound',
        kind='fiat',
        symbol='GBP',
        native=True,
        disabled=False,
        disabled_message=None,
        merchant=CurrencyMerchant(price=True, pay=False, receive=True),
        platforms=None
    ),
    Currency(
        id=5,
        title='Ethereum',
        kind='crypto',
        symbol='ETH',
        native=True,
        disabled=False,
        disabled_message=None,
        merchant=CurrencyMerchant(price=True, pay=True, receive=True),
        platforms=[
            CurrencyPlatform(id=2, id_name='binance_chain', title='Binance Chain (BEP2)', enabled=True),
            CurrencyPlatform(id=7, id_name='ethereum', title='Ethereum', enabled=True)
        ]
    )
]
```

### Platforms
Get all platforms

```py
>>> client.public.get_platforms(enabled=True)
[
    Platform(
        id=1,
        title='Ethereum (ERC20)',
        id_name='ethereum',
        disabled=False,
        disabled_message=None,
        currencies=[
            PlatformCurrency(id=50, title='Ethereum', symbol='ETH', enabled=True),
            PlatformCurrency(id=61, title='DAI', symbol='DAI', enabled=True),
            PlatformCurrency(id=71, title='Basic Attention Token', symbol='BAT', enabled=True)
        ]
    ),
    Platform(
        id=2,
        title='Binance Chain (BEP2)',
        id_name='binance_chain',
        disabled=False,
        disabled_message=None,
        currencies=[
            PlatformCurrency(id=50, title='Ethereum', symbol='ETH', enabled=True)
            PlatformCurrency(id=91, title='Binance Coin', symbol='BNB', enabled=True)
        ]
    )
]
```

## Custom Request Timeout
To modify request timeout time, you need to call method which will change it.

```py
>>> from coingate import CoinGate
>>> client = CoinGate("YOUR_API_TOKEN", True)
>>> client.set_timeout(10)
```

## Setting API Key after initialization
If you decided to initialize client without API Key and you need to do it later, you can call method which will update auth headers.

```py
>>> from coingate import Coingate
>>> client = CoinGate()
>>> client.public.ping()
Ping(ping='pong', time='2017-12-13T19:07:18+00:00')
>>> client.set_api_key('YOUR_API_KEY')
```
