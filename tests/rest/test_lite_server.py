# This file is auto-generated. Do not edit manually.
from tests.conftest import TestTonapiRest
from tests.rest.fixtures import params


class TestLiteServerResource(TestTonapiRest):
    async def test_get_raw_masterchain_info(self):
        response = await self.tonapi.lite_server.get_raw_masterchain_info()
        self.assertIsInstance(response, dict)

    async def test_get_raw_masterchain_info_ext(self):
        p = params("lite_server.get_raw_masterchain_info_ext")
        response = await self.tonapi.lite_server.get_raw_masterchain_info_ext(
            p["mode"],
        )
        self.assertIsInstance(response, dict)

    async def test_get_raw_time(self):
        response = await self.tonapi.lite_server.get_raw_time()
        self.assertIsInstance(response, dict)

    async def test_get_raw_blockchain_block(self):
        p = params("lite_server.get_raw_blockchain_block")
        response = await self.tonapi.lite_server.get_raw_blockchain_block(
            p["block_id"],
        )
        self.assertIsInstance(response, dict)

    # async def test_get_raw_blockchain_block_state(self):
    #     p = params("lite_server.get_raw_blockchain_block_state")
    #     response = await self.tonapi.lite_server.get_raw_blockchain_block_state(
    #         p["block_id"],
    #     )
    #     self.assertIsInstance(response, dict)

    async def test_get_raw_blockchain_block_header(self):
        p = params("lite_server.get_raw_blockchain_block_header")
        response = await self.tonapi.lite_server.get_raw_blockchain_block_header(
            p["block_id"],
            p["mode"],
        )
        self.assertIsInstance(response, dict)

    # async def test_send_raw_message(self):
    #     p = params("lite_server.send_raw_message")
    #     response = await self.tonapi.lite_server.send_raw_message(
    #         body=p["body"],
    #     )
    #     self.assertIsInstance(response, dict)

    async def test_get_raw_account_state(self):
        p = params("lite_server.get_raw_account_state")
        response = await self.tonapi.lite_server.get_raw_account_state(
            p["account_id"],
        )
        self.assertIsInstance(response, dict)

    async def test_get_raw_shard_info(self):
        p = params("lite_server.get_raw_shard_info")
        response = await self.tonapi.lite_server.get_raw_shard_info(
            p["block_id"],
            p["workchain"],
            p["shard"],
            p["exact"],
        )
        self.assertIsInstance(response, dict)

    async def test_get_all_raw_shards_info(self):
        p = params("lite_server.get_all_raw_shards_info")
        response = await self.tonapi.lite_server.get_all_raw_shards_info(
            p["block_id"],
        )
        self.assertIsInstance(response, dict)

    # async def test_get_raw_transactions(self):
    #     p = params("lite_server.get_raw_transactions")
    #     response = await self.tonapi.lite_server.get_raw_transactions(
    #         p["account_id"],
    #         p["count"],
    #         p["lt"],
    #         p["hash"],
    #     )
    #     self.assertIsInstance(response, dict)

    async def test_get_raw_list_block_transactions(self):
        p = params("lite_server.get_raw_list_block_transactions")
        response = await self.tonapi.lite_server.get_raw_list_block_transactions(
            p["block_id"],
            p["mode"],
            p["count"],
        )
        self.assertIsInstance(response, dict)

    async def test_get_raw_block_proof(self):
        p = params("lite_server.get_raw_block_proof")
        response = await self.tonapi.lite_server.get_raw_block_proof(
            p["known_block"],
            p["mode"],
        )
        self.assertIsInstance(response, dict)

    async def test_get_raw_config(self):
        p = params("lite_server.get_raw_config")
        response = await self.tonapi.lite_server.get_raw_config(
            p["block_id"],
            p["mode"],
        )
        self.assertIsInstance(response, dict)

    async def test_get_raw_shard_block_proof(self):
        p = params("lite_server.get_raw_shard_block_proof")
        response = await self.tonapi.lite_server.get_raw_shard_block_proof(
            p["block_id"],
        )
        self.assertIsInstance(response, dict)

    async def test_get_out_msg_queue_sizes(self):
        response = await self.tonapi.lite_server.get_out_msg_queue_sizes()
        self.assertIsInstance(response, dict)
