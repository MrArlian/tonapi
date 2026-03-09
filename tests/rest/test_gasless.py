# This file is auto-generated. Do not edit manually.

from pytonapi.rest.models import GaslessConfig
from tests.conftest import TestTonapiRest


class TestGaslessResource(TestTonapiRest):
    async def test_config(self):
        response = await self.tonapi.gasless.config()
        self.assertIsInstance(response, GaslessConfig)

    # async def test_estimate(self):
    #     p = params("gasless.estimate")
    #     response = await self.tonapi.gasless.estimate(
    #         p["master_id"],
    #         body=p["body"],
    #     )
    #     self.assertIsInstance(response, SignRawParams)

    # async def test_send(self):
    #     p = params("gasless.send")
    #     response = await self.tonapi.gasless.send(
    #         body=p["body"],
    #     )
    #     self.assertIsInstance(response, GaslessTx)
