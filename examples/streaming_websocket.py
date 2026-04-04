import asyncio

from pytonapi.streaming import TonapiStreaming
from pytonapi.types import Network, Opcode, Workchain

# TONAPI key — get one at https://tonconsole.com/
API_KEY = "YOUR_API_KEY"

# Target network — MAINNET or TESTNET
NETWORK = Network.MAINNET

# Account address to track — raw format
ACCOUNT_ID = "0:408da3b28b6c065a593e10391269baaa9c5f8caebc0c69d9f0aabbab2a99256b"

# Duration for each subscription demo (seconds)
DURATION = 30


def make_stop(seconds: float) -> asyncio.Event:
    """Create a stop event that fires after *seconds*."""
    event = asyncio.Event()

    async def _set_after() -> None:
        await asyncio.sleep(seconds)
        event.set()

    asyncio.ensure_future(_set_after())
    return event


async def main() -> None:
    async with TonapiStreaming(API_KEY, NETWORK) as streaming:
        # 1. Finalized transactions via WebSocket JSON-RPC
        # accounts=None subscribes to ALL accounts
        # operations filters by opcode (e.g., Opcode.JETTON_TRANSFER)
        print("— Subscribing to transactions...")
        async for event in streaming.ws.subscribe_transactions(
            accounts=[ACCOUNT_ID],
            operations=[Opcode.TEXT_COMMENT],
            stop=make_stop(DURATION),
        ):
            print(f"TX: {event.account_id} | {event.tx_hash}")

        # 2. New blocks via WebSocket
        # workchain=None subscribes to blocks from all workchains
        print("— Subscribing to blocks...")
        async for block in streaming.ws.subscribe_blocks(
            workchain=Workchain.MASTERCHAIN,
            stop=make_stop(DURATION),
        ):
            print(f"Block: {block.workchain} | {block.seqno}")

        # 3. Completed traces via WebSocket
        # accounts=None subscribes to ALL traces
        print("— Subscribing to traces...")
        async for trace in streaming.ws.subscribe_traces(
            accounts=[ACCOUNT_ID],
            stop=make_stop(DURATION),
        ):
            print(f"Trace: {trace.hash}")

        # 4. Pending messages via WebSocket
        # accounts filters by involved accounts after emulation
        # accounts=None subscribes to ALL pending messages (high volume!)
        print("— Subscribing to mempool...")
        async for msg in streaming.ws.subscribe_mempool(
            stop=make_stop(DURATION),
        ):
            print(f"Mempool: {msg.boc}")


if __name__ == "__main__":
    asyncio.run(main())
