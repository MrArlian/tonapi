# This file is auto-generated. Do not edit manually.

from pytonapi.rest.models import Seqno, Wallet, Wallets, WalletsByPublicKeys
from tests.conftest import TestTonapiRest
from tests.rest.fixtures import params


class TestWalletResource(TestTonapiRest):
    # async def test_ton_connect_proof(self):
    #     p = params("wallet.ton_connect_proof")
    #     response = await self.tonapi.wallet.ton_connect_proof(
    #         body=p["body"],
    #     )
    #     self.assertIsInstance(response, dict)

    async def test_get_account_seqno(self):
        p = params("wallet.get_account_seqno")
        response = await self.tonapi.wallet.get_account_seqno(
            p["account_id"],
        )
        self.assertIsInstance(response, Seqno)

    async def test_get_info(self):
        p = params("wallet.get_info")
        response = await self.tonapi.wallet.get_info(
            p["account_id"],
        )
        self.assertIsInstance(response, Wallet)

    async def test_get_wallets_by_public_key(self):
        p = params("wallet.get_wallets_by_public_key")
        response = await self.tonapi.wallet.get_wallets_by_public_key(
            p["public_key"],
        )
        self.assertIsInstance(response, Wallets)

    async def test_get_wallets_by_public_key_bulk(self):
        p = params("wallet.get_wallets_by_public_key_bulk")
        response = await self.tonapi.wallet.get_wallets_by_public_key_bulk(
            body=p["body"],
        )
        self.assertIsInstance(response, WalletsByPublicKeys)

    # async def test_emulate_message_to_wallet(self):
    #     p = params("wallet.emulate_message_to_wallet")
    #     response = await self.tonapi.wallet.emulate_message_to_wallet(
    #         body=p["body"],
    #     )
    #     self.assertIsInstance(response, MessageConsequences)
