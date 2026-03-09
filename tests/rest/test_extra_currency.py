# This file is auto-generated. Do not edit manually.

from pytonapi.rest.models import EcPreview
from tests.conftest import TestTonapiRest
from tests.rest.fixtures import params


class TestExtraCurrencyResource(TestTonapiRest):
    async def test_get_info(self):
        p = params("extra_currency.get_info")
        response = await self.tonapi.extra_currency.get_info(
            p["id"],
        )
        self.assertIsInstance(response, EcPreview)
