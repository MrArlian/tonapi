# This file is auto-generated. Do not edit manually.

from pytonapi.rest.models import AccountInfoByStateInit
from tests.conftest import TestTonapiRest
from tests.rest.fixtures import params


class TestConnectResource(TestTonapiRest):
    async def test_get_ton_connect_payload(self):
        response = await self.tonapi.connect.get_ton_connect_payload()
        self.assertIsInstance(response, dict)

    async def test_get_account_info_by_state_init(self):
        p = params("connect.get_account_info_by_state_init")
        response = await self.tonapi.connect.get_account_info_by_state_init(
            body=p["body"],
        )
        self.assertIsInstance(response, AccountInfoByStateInit)
