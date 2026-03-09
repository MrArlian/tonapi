# This file is auto-generated. Do not edit manually.
from tests.conftest import TestTonapiRest


class TestStorageResource(TestTonapiRest):
    async def test_get_providers(self):
        response = await self.tonapi.storage.get_providers()
        self.assertIsInstance(response, dict)
