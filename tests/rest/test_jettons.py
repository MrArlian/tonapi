# This file is auto-generated. Do not edit manually.

from pytonapi.rest.models import Event, JettonHolders, JettonInfo, Jettons
from tests.conftest import TestTonapiRest
from tests.rest.fixtures import params


class TestJettonsResource(TestTonapiRest):
    async def test_get_jettons(self):
        response = await self.tonapi.jettons.get_jettons()
        self.assertIsInstance(response, Jettons)

    async def test_get_jetton_info(self):
        p = params("jettons.get_jetton_info")
        response = await self.tonapi.jettons.get_jetton_info(
            p["account_id"],
        )
        self.assertIsInstance(response, JettonInfo)

    async def test_get_jetton_infos_by_addresses(self):
        p = params("jettons.get_jetton_infos_by_addresses")
        response = await self.tonapi.jettons.get_jetton_infos_by_addresses(
            body=p["body"],
        )
        self.assertIsInstance(response, Jettons)

    async def test_get_jetton_holders(self):
        p = params("jettons.get_jetton_holders")
        response = await self.tonapi.jettons.get_jetton_holders(
            p["account_id"],
        )
        self.assertIsInstance(response, JettonHolders)

    # async def test_get_jetton_transfer_payload(self):
    #     p = params("jettons.get_jetton_transfer_payload")
    #     response = await self.tonapi.jettons.get_jetton_transfer_payload(
    #         p["account_id"],
    #         p["jetton_id"],
    #     )
    #     self.assertIsInstance(response, JettonTransferPayload)

    async def test_get_events(self):
        p = params("jettons.get_events")
        response = await self.tonapi.jettons.get_events(
            p["event_id"],
        )
        self.assertIsInstance(response, Event)
