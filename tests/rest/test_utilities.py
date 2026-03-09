# This file is auto-generated. Do not edit manually.

from pytonapi.rest.models import ServiceStatus
from tests.conftest import TestTonapiRest
from tests.rest.fixtures import params


class TestUtilitiesResource(TestTonapiRest):
    async def test_get_openapi_json(self):
        response = await self.tonapi.utilities.get_openapi_json()
        self.assertIsInstance(response, dict)

    async def test_get_openapi_yml(self):
        response = await self.tonapi.utilities.get_openapi_yml()
        self.assertIsInstance(response, str)

    async def test_status(self):
        response = await self.tonapi.utilities.status()
        self.assertIsInstance(response, ServiceStatus)

    async def test_address_parse(self):
        p = params("utilities.address_parse")
        response = await self.tonapi.utilities.address_parse(
            p["account_id"],
        )
        self.assertIsInstance(response, dict)
