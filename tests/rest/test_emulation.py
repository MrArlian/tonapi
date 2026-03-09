# This file is auto-generated. Do not edit manually.

from pytonapi.rest.models import DecodedMessage
from tests.conftest import TestTonapiRest
from tests.rest.fixtures import params


class TestEmulationResource(TestTonapiRest):
    async def test_decode_message(self):
        p = params("emulation.decode_message")
        response = await self.tonapi.emulation.decode_message(
            body=p["body"],
        )
        self.assertIsInstance(response, DecodedMessage)

    # async def test_emulate_message_to_event(self):
    #     p = params("emulation.emulate_message_to_event")
    #     response = await self.tonapi.emulation.emulate_message_to_event(
    #         body=p["body"],
    #     )
    #     self.assertIsInstance(response, Event)

    # async def test_emulate_message_to_trace(self):
    #     p = params("emulation.emulate_message_to_trace")
    #     response = await self.tonapi.emulation.emulate_message_to_trace(
    #         body=p["body"],
    #     )
    #     self.assertIsInstance(response, Trace)

    # async def test_emulate_message_to_wallet(self):
    #     p = params("emulation.emulate_message_to_wallet")
    #     response = await self.tonapi.emulation.emulate_message_to_wallet(
    #         body=p["body"],
    #     )
    #     self.assertIsInstance(response, MessageConsequences)

    # async def test_emulate_message_to_account_event(self):
    #     p = params("emulation.emulate_message_to_account_event")
    #     response = await self.tonapi.emulation.emulate_message_to_account_event(
    #         p["account_id"],
    #         body=p["body"],
    #     )
    #     self.assertIsInstance(response, AccountEvent)
