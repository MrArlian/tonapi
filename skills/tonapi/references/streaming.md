# Streaming

Real-time event subscriptions via SSE or WebSocket. Both transports return async iterators.

## TonapiStreaming Constructor

```python
from pytonapi.streaming import TonapiStreaming
from pytonapi.types import Network

streaming = TonapiStreaming(
    api_key: str,
    network: Network,
    *,
    base_url: str | None = None,
    headers: dict[str, str] | None = None,
    reconnect_policy: ReconnectPolicy = DEFAULT_RECONNECT_POLICY,
)
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| api_key | str | — | API key from [tonconsole.com](https://tonconsole.com/) |
| network | `Network` | — | `Network.MAINNET`, `Network.TESTNET`, or `Network.TETRA` |
| base_url | str \| None | None | Custom base URL (overrides network) |
| headers | dict \| None | None | Additional HTTP headers |
| reconnect_policy | `ReconnectPolicy` | default | Reconnect policy (max 10, 0.5s delay, 2x backoff) |

Access transports via properties: `streaming.sse` and `streaming.ws`.

Use as context manager:

```python
async with TonapiStreaming("api_key", Network.MAINNET) as streaming:
    async for event in streaming.sse.subscribe_transactions(...):
        ...
```

Or explicit lifecycle:

```python
streaming = TonapiStreaming("api_key", Network.MAINNET)
await streaming.create_session()
try:
    async for event in streaming.sse.subscribe_transactions(...):
        ...
finally:
    await streaming.close_session()
```

## SSE Subscriptions

### subscribe_transactions

Subscribe to new transactions in real-time.

```python
async for event in streaming.sse.subscribe_transactions(
    accounts: list[str] | None = None,
    operations: list[str] | None = None,
    stop: asyncio.Event | None = None,
) -> AsyncIterator[TransactionEvent]:
    print(event.account_id, event.tx_hash)
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| accounts | list[str] \| None | None | Account addresses to monitor (any format) |
| operations | list[str] \| None | None | Filter by operation codes (hex, e.g. `"0x0f8a7ea5"`) |
| stop | asyncio.Event \| None | None | Set to stop the subscription |

Returns: `AsyncIterator[TransactionEvent]`

### subscribe_blocks

Subscribe to new blocks.

```python
async for event in streaming.sse.subscribe_blocks(
    workchain: Workchain | None = None,
    stop: asyncio.Event | None = None,
) -> AsyncIterator[BlockEvent]:
    print(event.workchain, event.seqno)
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| workchain | `Workchain` \| None | None | Filter by workchain (`Workchain.MASTERCHAIN` or `Workchain.BASECHAIN`) |
| stop | asyncio.Event \| None | None | Set to stop the subscription |

Returns: `AsyncIterator[BlockEvent]`

### subscribe_traces

Subscribe to execution traces.

```python
async for event in streaming.sse.subscribe_traces(
    accounts: list[str] | None = None,
    stop: asyncio.Event | None = None,
) -> AsyncIterator[TraceEvent]:
    print(event.hash, event.accounts)
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| accounts | list[str] \| None | None | Account addresses to monitor |
| stop | asyncio.Event \| None | None | Set to stop the subscription |

Returns: `AsyncIterator[TraceEvent]`

### subscribe_mempool

Subscribe to mempool messages.

```python
async for event in streaming.sse.subscribe_mempool(
    accounts: list[str] | None = None,
    stop: asyncio.Event | None = None,
) -> AsyncIterator[MempoolEvent]:
    print(event.boc)
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| accounts | list[str] \| None | None | Account addresses to monitor |
| stop | asyncio.Event \| None | None | Set to stop the subscription |

Returns: `AsyncIterator[MempoolEvent]`

## WebSocket Subscriptions

WebSocket transport (`streaming.ws`) has the same four methods with identical signatures:

- `subscribe_transactions(accounts, operations, stop)`
- `subscribe_blocks(workchain, stop)`
- `subscribe_traces(accounts, stop)`
- `subscribe_mempool(accounts, stop)`

SSE is simpler (one-way, POST-based). WebSocket is bidirectional.

## Event Models

| Model | Fields |
|-------|--------|
| `TransactionEvent` | `account_id: str`, `lt: int`, `tx_hash: str` |
| `BlockEvent` | `workchain: int`, `shard: str`, `seqno: int`, `root_hash: str`, `file_hash: str` |
| `TraceEvent` | `accounts: list[str]`, `hash: str` |
| `MempoolEvent` | `boc: str`, `involved_accounts: list[str] \| None` |

All models are Pydantic `BaseModel` subclasses with `model_dump_json()` support.

## Stopping a Subscription

Use `asyncio.Event` to signal stop:

```python
stop = asyncio.Event()

async def stop_after(seconds: float) -> None:
    await asyncio.sleep(seconds)
    stop.set()

asyncio.create_task(stop_after(30))

async for event in streaming.sse.subscribe_transactions(
    accounts=["EQ..."],
    stop=stop,
):
    print(event)
```

## ReconnectPolicy

```python
from pytonapi.types import ReconnectPolicy

policy = ReconnectPolicy(
    max_reconnects=10,   # max attempts before giving up (-1 for unlimited)
    delay=0.5,           # initial delay in seconds
    max_delay=10.0,      # maximum delay
    backoff_factor=2.0,  # exponential backoff multiplier
)

streaming = TonapiStreaming("api_key", Network.MAINNET, reconnect_policy=policy)
```

Default: `max_reconnects=10, delay=0.5, max_delay=10.0, backoff_factor=2.0`.

## Opcode Filtering

Filter transactions by opcode using the `operations` parameter:

```python
from pytonapi.types import Opcode

async for event in streaming.sse.subscribe_transactions(
    accounts=["EQ..."],
    operations=[Opcode.JETTON_TRANSFER, Opcode.JETTON_NOTIFY],
):
    print(f"Jetton activity: {event.tx_hash}")
```

Well-known opcodes are available in the `Opcode` enum (50+ entries including `JETTON_TRANSFER`, `NFT_TRANSFER`, `MULTISIG_NEW_ORDER`, etc.).

## Runner Example

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py streaming sse \
    --accounts EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2 \
    --subscribe transactions \
    --duration 30

python3 ${CLAUDE_SKILL_DIR}/scripts/run.py streaming ws \
    --accounts EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2 \
    --subscribe transactions,blocks \
    --duration 60
```

Runner streaming params: `--subscribe` (comma-separated: transactions, blocks, traces, mempool), `--accounts`, `--operations`, `--workchain`, `--duration` (seconds, default 60).
