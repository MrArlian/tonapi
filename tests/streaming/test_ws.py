from pytonapi.streaming.models import (
    BlockEvent,
    MempoolEvent,
    TraceEvent,
    TransactionEvent,
)
from pytonapi.types import Workchain
from tests.conftest import TestTonapiStreaming

ACCOUNT_ID = "0:83ae019a23a8162beaa5cb0ebdc56668b2eac6c6ba51808812915b206a152dc5"
DURATION = 30


class TestWS(TestTonapiStreaming):
    async def test_subscribe_transactions(self) -> None:
        count = 0
        async for event in self.streaming.ws.subscribe_transactions(
            accounts=[ACCOUNT_ID],
            stop=self.make_stop(DURATION),
        ):
            self.assertIsInstance(event, TransactionEvent)
            self.assertTrue(event.account_id)
            self.assertTrue(event.tx_hash)
            self.assertGreater(event.lt, 0)
            count += 1
        print(f"WS transactions: {count} events")

    async def test_subscribe_blocks(self) -> None:
        count = 0
        async for block in self.streaming.ws.subscribe_blocks(
            workchain=Workchain.MASTERCHAIN,
            stop=self.make_stop(DURATION),
        ):
            self.assertIsInstance(block, BlockEvent)
            self.assertEqual(block.workchain, Workchain.MASTERCHAIN)
            self.assertTrue(block.shard)
            self.assertGreater(block.seqno, 0)
            count += 1
        print(f"WS blocks: {count} events")

    async def test_subscribe_traces(self) -> None:
        count = 0
        async for trace in self.streaming.ws.subscribe_traces(
            accounts=[ACCOUNT_ID],
            stop=self.make_stop(DURATION),
        ):
            self.assertIsInstance(trace, TraceEvent)
            self.assertTrue(trace.hash)
            self.assertIsInstance(trace.accounts, list)
            count += 1
        print(f"WS traces: {count} events")

    async def test_subscribe_mempool(self) -> None:
        count = 0
        async for msg in self.streaming.ws.subscribe_mempool(
            stop=self.make_stop(DURATION),
        ):
            self.assertIsInstance(msg, MempoolEvent)
            self.assertTrue(msg.boc)
            count += 1
        print(f"WS mempool: {count} events")
