# This file is auto-generated. Do not edit manually.
from tests.conftest import TestTonapiRest
from tests.rest.fixtures import params


class TestRatesResource(TestTonapiRest):
    async def test_get_rates(self):
        p = params("rates.get_rates")
        response = await self.tonapi.rates.get_rates(
            p["tokens"],
            p["currencies"],
        )
        self.assertIsInstance(response, dict)

    async def test_get_chart_rates(self):
        p = params("rates.get_chart_rates")
        response = await self.tonapi.rates.get_chart_rates(
            p["token"],
        )
        self.assertIsInstance(response, dict)

    async def test_get_markets_rates(self):
        response = await self.tonapi.rates.get_markets_rates()
        self.assertIsInstance(response, dict)
