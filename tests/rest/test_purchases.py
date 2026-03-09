# This file is auto-generated. Do not edit manually.

from pytonapi.rest.models import AccountPurchases
from tests.conftest import TestTonapiRest
from tests.rest.fixtures import params


class TestPurchasesResource(TestTonapiRest):
    async def test_get_purchase_history(self):
        p = params("purchases.get_purchase_history")
        response = await self.tonapi.purchases.get_purchase_history(
            p["account_id"],
        )
        self.assertIsInstance(response, AccountPurchases)
