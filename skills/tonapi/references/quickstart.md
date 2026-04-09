# Quickstart

## Installation

```bash
pip install pytonapi
```

## Configuration

Environment variables (used by the runner script):

| Variable | Description | Default |
|---|---|---|
| `TONAPI_NETWORK` | `mainnet`, `testnet`, or `tetra` | `mainnet` |
| `TONAPI_API_KEY` | API key (optional — unlocks higher rate limits) | — |
| `TONAPI_BASE_URL` | Custom base URL (overrides network) | — |
| `TONAPI_RPS_LIMIT` | Max requests per period | — |
| `TONAPI_RPS_PERIOD` | Rate limit period in seconds | — |

API key is optional — without a key, REST requests are throttled to ~1 per 4 seconds. A key unlocks higher rate limits. Get one at [tonconsole.com](https://tonconsole.com/).

## First REST Request

```python
import asyncio
from pytonapi.rest import TonapiRestClient
from pytonapi.types import Network

async def main() -> None:
    async with TonapiRestClient("your_api_key", Network.MAINNET) as tonapi:
        account = await tonapi.accounts.get_account(
            "EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2"
        )
        print(account.model_dump_json(indent=2))

asyncio.run(main())
```

Without API key (~1 request per 4 seconds):

```python
async with TonapiRestClient(network=Network.MAINNET) as tonapi:
    account = await tonapi.accounts.get_account("EQ...")
    print(account.model_dump_json(indent=2))
```

With rate limit and custom timeout:

```python
async with TonapiRestClient(
    "your_api_key",
    Network.MAINNET,
    rps_limit=10,
    timeout=30.0,
) as tonapi:
    ...
```

Without context manager (explicit lifecycle):

```python
tonapi = TonapiRestClient("your_api_key", Network.MAINNET)
await tonapi.create_session()
try:
    account = await tonapi.accounts.get_account("EQ...")
finally:
    await tonapi.close_session()
```

## First Streaming Subscription

```python
import asyncio
from pytonapi.streaming import Finality, TonapiSSE, TransactionsNotification
from pytonapi.types import Network

client = TonapiSSE("your_api_key", Network.MAINNET)

@client.on_transactions(min_finality=Finality.FINALIZED)
async def handle_tx(event: TransactionsNotification) -> None:
    for tx in event.transactions:
        print(tx)

async def main() -> None:
    try:
        await client.start(addresses=["EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2"])
    finally:
        await client.stop()

asyncio.run(main())
```

## First Webhook

```python
from pytonapi.webhook import TonapiWebhookClient, TonapiWebhookDispatcher
from pytonapi.webhook import AccountTxEvent
from pytonapi.types import Network

client = TonapiWebhookClient("your_api_key", Network.MAINNET)
dispatcher = TonapiWebhookDispatcher(
    "https://example.com/webhook",
    client=client,
    accounts=["EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2"],
)

@dispatcher.account_tx()
async def handle_tx(event: AccountTxEvent) -> None:
    print(f"TX: {event.tx_hash}")

# Call dispatcher.setup() at startup, dispatcher.teardown() at shutdown
# See references/webhooks.md for full FastAPI/aiohttp integration examples
```

## Custom Endpoint

For custom TONAPI instances, pass `base_url`:

```python
async with TonapiRestClient(
    "your_api_key",
    Network.MAINNET,
    base_url="https://my-tonapi.example.com",
) as tonapi:
    ...
```

## Utility Functions

```python
from pytonapi.utils import raw_to_userfriendly, userfriendly_to_raw, to_nano, to_amount
```

### `raw_to_userfriendly`

Convert raw address (`workchain:hex`) to user-friendly base64 format.

```python
raw_to_userfriendly(
    address: str,
    is_bounceable: bool = False,
    is_url_safe: bool = True,
    is_test_only: bool = False,
) -> str
```

### `userfriendly_to_raw`

Convert user-friendly base64 address to raw format.

```python
userfriendly_to_raw(address: str) -> str
```

Raises `ValueError` on invalid length, CRC, or tag.

### `to_nano`

Convert human-readable amount to smallest units (nanotons).

```python
to_nano(
    value: int | float | str | decimal.Decimal,
    decimals: int = 9,
) -> int
```

Example: `to_nano(1.5)` → `1500000000`

### `to_amount`

Convert smallest units to human-readable `Decimal`.

```python
to_amount(
    value: int,
    decimals: int = 9,
    *,
    precision: int | None = None,
) -> decimal.Decimal
```

Example: `to_amount(1500000000)` → `Decimal('1.5')`

## Error Handling

All SDK exceptions inherit from `TONAPIError`:

- `TONAPIConnectionError` — network-level failures
- `TONAPIClientError` — 4xx HTTP (bad request, unauthorized, not found, rate limit)
- `TONAPIServerError` — 5xx HTTP (internal error)
- `TONAPISessionNotCreatedError` — session not created before request
- `TONAPIStreamingError` — streaming transport error
- `TONAPIConnectionLostError` — reconnect limit exhausted during streaming

- `TONAPIValidationError` — response body did not match expected Pydantic model
- `TONAPIRetryLimitError` — all retry attempts exhausted

```python
from pytonapi.exceptions import TONAPIError, TONAPINotFoundError

try:
    result = await tonapi.accounts.get_account(address)
except TONAPINotFoundError:
    print("Address not found")
except TONAPIError as e:
    print(f"API error: {e}")
```
