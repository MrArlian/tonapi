# Webhooks

Push notifications for TON blockchain events. Two main components: `TonapiWebhookClient` for CRUD operations and `TonapiWebhookDispatcher` for event dispatch with decorators.

## TonapiWebhookClient

HTTP client for managing webhook subscriptions.

```python
from pytonapi.webhook import TonapiWebhookClient
from pytonapi.types import Network

client = TonapiWebhookClient(
    api_key: str,
    network: Network,
    *,
    base_url: str | None = None,
    timeout: float = 10.0,
    session: aiohttp.ClientSession | None = None,
    headers: dict[str, str] | None = None,
    cookies: dict[str, str] | None = None,
    retry_policy: RetryPolicy | None = DEFAULT_RETRY_POLICY,
)
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| api_key | str | — | API key from [tonconsole.com](https://tonconsole.com/) |
| network | `Network` | — | `Network.MAINNET` or `Network.TESTNET` |
| base_url | str \| None | None | Custom base URL (overrides network) |
| timeout | float | 10.0 | Request timeout in seconds |
| session | ClientSession \| None | None | External session (not closed by client) |
| headers | dict \| None | None | Additional HTTP headers |
| cookies | dict \| None | None | Additional cookies |
| retry_policy | RetryPolicy \| None | default | Retry policy, or None to disable |

### create

Create a new webhook.

```python
webhook = await client.create(endpoint="https://example.com/webhook")
```

Returns: `TonapiWebhook`

### list

List all webhooks.

```python
webhooks = await client.list()
```

Returns: `list[WebhookInfo]`

### delete

Delete a webhook by ID.

```python
await client.delete(webhook_id=123)
```

### get_info

Get webhook details by ID.

```python
info = await client.get_info(webhook_id=123)
```

Returns: `WebhookInfo`

### get

Get a bound webhook object by ID.

```python
webhook = await client.get(webhook_id=123)
```

Returns: `TonapiWebhook`

### ensure

Get or create a webhook for the given endpoint.

```python
webhook = await client.ensure(endpoint="https://example.com/webhook")
```

Returns: `TonapiWebhook`

## TonapiWebhook

Bound webhook instance with subscribe/unsubscribe methods.

Properties: `id: int`, `endpoint: str`, `token: str`

### subscribe / unsubscribe

```python
await webhook.subscribe(accounts=["EQ..."])
await webhook.unsubscribe(accounts=["EQ..."])
```

### get_subscriptions

```python
subs = await webhook.get_subscriptions(offset=0, limit=10)
```

Returns: `list[AccountSubscription]`

### subscribe_new_contracts / unsubscribe_new_contracts

```python
await webhook.subscribe_new_contracts()
await webhook.unsubscribe_new_contracts()
```

### subscribe_mempool_msg / unsubscribe_mempool_msg

```python
await webhook.subscribe_mempool_msg()
await webhook.unsubscribe_mempool_msg()
```

### subscribe_opcode_msg / unsubscribe_opcode_msg

```python
await webhook.subscribe_opcode_msg(opcode="0x0f8a7ea5")
await webhook.unsubscribe_opcode_msg(opcode="0x0f8a7ea5")
```

### sync_accounts

Replace all subscriptions with the given account list.

```python
await webhook.sync_accounts(accounts=["EQ..."])
```

### delete

```python
await webhook.delete()
```

## TonapiWebhookDispatcher

Event dispatcher with decorator-based handler registration. Integrates with web frameworks (FastAPI, aiohttp).

```python
from pytonapi.webhook import TonapiWebhookDispatcher, TonapiWebhookClient

dispatcher = TonapiWebhookDispatcher(
    url: str = "",
    *,
    client: TonapiWebhookClient | None = None,
    accounts: list[str] | None = None,
    opcodes: list[str] | None = None,
    **kwargs,
)
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| url | str | `""` | Public URL for the webhook endpoint |
| client | TonapiWebhookClient \| None | None | Webhook client (required for setup/teardown) |
| accounts | list[str] \| None | None | Accounts to subscribe to |
| opcodes | list[str] \| None | None | Opcodes for opcode_msg subscriptions |

### Decorator Handlers

Register handlers before calling `setup()`.

#### @dispatcher.account_tx()

```python
@dispatcher.account_tx()
async def handle(event: AccountTxEvent) -> None:
    print(event.account_id, event.tx_hash)
```

With account filter and custom path:

```python
@dispatcher.account_tx("EQ...", "EQ...", path="/custom-path")
async def handle(event: AccountTxEvent) -> None:
    ...
```

#### @dispatcher.mempool_msg()

```python
@dispatcher.mempool_msg()
async def handle(event: MempoolMsgEvent) -> None:
    print(event.boc)
```

#### @dispatcher.opcode_msg()

```python
@dispatcher.opcode_msg()
async def handle(event: OpcodeMsgEvent) -> None:
    print(event.account_id, event.tx_hash)
```

#### @dispatcher.new_contracts()

```python
@dispatcher.new_contracts()
async def handle(event: NewContractsEvent) -> None:
    print(event.account_id)
```

### setup / teardown

```python
await dispatcher.setup()    # creates webhooks, subscribes
await dispatcher.teardown(cleanup=False)  # closes session; cleanup=True unsubscribes first
```

### process

Dispatch incoming webhook data to registered handlers.

```python
await dispatcher.process(
    path="/account-tx",
    data=request_json,
    authorization=request_headers.get("Authorization"),
)
```

### paths

Get registered paths and their event types.

```python
dispatcher.paths  # -> dict[WebhookEventType, str]
```

Default URL suffixes: `/account-tx`, `/mempool-msg`, `/opcode-msg`, `/new-contracts`.

## Event Models

| Model | Fields |
|-------|--------|
| `AccountTxEvent` | `event_type: "account_tx"`, `account_id: str`, `lt: int`, `tx_hash: str` |
| `MempoolMsgEvent` | `event_type: "mempool_msg"`, `boc: str` |
| `OpcodeMsgEvent` | `event_type: "opcode_msg"`, `account_id: str`, `lt: int`, `tx_hash: str` |
| `NewContractsEvent` | `event_type: "new_contracts"`, `account_id: str`, `lt: int`, `tx_hash: str` |

## WebhookInfo Fields

`id`, `endpoint`, `token`, `subscribed_accounts`, `subscribed_msg_opcodes`, `subscribed_to_mempool`, `subscribed_to_new_contracts`, `status`, `status_updated_at`, `last_online_at`, `status_failed_attempts`.

## FastAPI Example

```python
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response

from pytonapi.types import Network, Opcode
from pytonapi.webhook import (
    AccountTxEvent,
    MempoolMsgEvent,
    NewContractsEvent,
    OpcodeMsgEvent,
    TonapiWebhookClient,
    TonapiWebhookDispatcher,
)

ACCOUNT_ID = "0:408da3b28b6c065a593e10391269baaa9c5f8caebc0c69d9f0aabbab2a99256b"

client = TonapiWebhookClient("api_key", Network.MAINNET)
dispatcher = TonapiWebhookDispatcher(
    "https://example.com/webhook",
    client=client,
    accounts=[ACCOUNT_ID],
    opcodes=[Opcode.TEXT_COMMENT],
)

@dispatcher.account_tx()
async def on_account_tx(event: AccountTxEvent) -> None:
    print(f"Account TX: {event.account_id} | {event.tx_hash}")

@dispatcher.mempool_msg()
async def on_mempool_msg(event: MempoolMsgEvent) -> None:
    print(f"Mempool: {event.boc}")

@dispatcher.opcode_msg()
async def on_opcode_msg(event: OpcodeMsgEvent) -> None:
    print(f"Opcode: {event.account_id} | {event.tx_hash}")

@dispatcher.new_contracts()
async def on_new_contract(event: NewContractsEvent) -> None:
    print(f"New contract: {event.account_id} | {event.tx_hash}")

async def handle_webhook(request: Request) -> Response:
    data = await request.json()
    try:
        authorization = request.headers.get("Authorization")
        await dispatcher.process(request.url.path, data, authorization=authorization)
    except Exception as e:
        print(f"Webhook error: {e}")
        return Response(status_code=401)
    return Response(status_code=200)

@asynccontextmanager
async def lifespan(application: FastAPI):
    try:
        await dispatcher.setup()
        for path in dispatcher.paths.values():
            application.add_api_route(path, handle_webhook, methods=["POST"])
        yield
    finally:
        await dispatcher.teardown()

app = FastAPI(lifespan=lifespan)
```

## aiohttp Example

```python
import asyncio

from aiohttp import web

from pytonapi.types import Network, Opcode
from pytonapi.webhook import (
    AccountTxEvent,
    TonapiWebhookClient,
    TonapiWebhookDispatcher,
)

ACCOUNT_ID = "0:408da3b28b6c065a593e10391269baaa9c5f8caebc0c69d9f0aabbab2a99256b"

client = TonapiWebhookClient("api_key", Network.MAINNET)
dispatcher = TonapiWebhookDispatcher(
    "https://example.com/webhook",
    client=client,
    accounts=[ACCOUNT_ID],
    opcodes=[Opcode.TEXT_COMMENT],
)

@dispatcher.account_tx()
async def on_account_tx(event: AccountTxEvent) -> None:
    print(f"Account TX: {event.account_id} | {event.tx_hash}")

async def handle_webhook(request: web.Request) -> web.Response:
    data = await request.json()
    try:
        authorization = request.headers.get("Authorization")
        await dispatcher.process(request.path, data, authorization=authorization)
    except Exception as e:
        print(f"Webhook error: {e}")
        return web.Response(status=401)
    return web.Response(status=200)

async def main() -> None:
    try:
        await dispatcher.setup()
        app = web.Application()
        for path in dispatcher.paths.values():
            app.router.add_post(path, handle_webhook)
        runner = web.AppRunner(app)
        await runner.setup()
        await web.TCPSite(runner, "0.0.0.0", 8000).start()
        await asyncio.Event().wait()
    finally:
        await dispatcher.teardown()

asyncio.run(main())
```
