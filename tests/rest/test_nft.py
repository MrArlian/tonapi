# This file is auto-generated. Do not edit manually.

from pytonapi.rest.models import AccountEvents, NftCollection, NftCollections, NftItem, NftItems, NftOperations
from tests.conftest import TestTonapiRest
from tests.rest.fixtures import params


class TestNFTResource(TestTonapiRest):
    async def test_get_account_nft_history(self):
        p = params("nft.get_account_nft_history")
        response = await self.tonapi.nft.get_account_nft_history(
            p["account_id"],
            p["limit"],
        )
        self.assertIsInstance(response, NftOperations)

    async def test_get_collections(self):
        response = await self.tonapi.nft.get_collections()
        self.assertIsInstance(response, NftCollections)

    async def test_get_collection(self):
        p = params("nft.get_collection")
        response = await self.tonapi.nft.get_collection(
            p["account_id"],
        )
        self.assertIsInstance(response, NftCollection)

    async def test_get_collection_items_by_addresses(self):
        p = params("nft.get_collection_items_by_addresses")
        response = await self.tonapi.nft.get_collection_items_by_addresses(
            body=p["body"],
        )
        self.assertIsInstance(response, NftCollections)

    async def test_get_items_from_collection(self):
        p = params("nft.get_items_from_collection")
        response = await self.tonapi.nft.get_items_from_collection(
            p["account_id"],
        )
        self.assertIsInstance(response, NftItems)

    async def test_get_items_by_addresses(self):
        p = params("nft.get_items_by_addresses")
        response = await self.tonapi.nft.get_items_by_addresses(
            body=p["body"],
        )
        self.assertIsInstance(response, NftItems)

    async def test_get_item_by_address(self):
        p = params("nft.get_item_by_address")
        response = await self.tonapi.nft.get_item_by_address(
            p["account_id"],
        )
        self.assertIsInstance(response, NftItem)

    async def test_get_history_by_id(self):
        p = params("nft.get_history_by_id")
        response = await self.tonapi.nft.get_history_by_id(
            p["account_id"],
            p["limit"],
        )
        self.assertIsInstance(response, AccountEvents)
