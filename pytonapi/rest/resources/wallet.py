# This file is auto-generated. Do not edit manually.

from __future__ import annotations

import typing as t

from pytonapi.rest.models import MessageConsequences, Seqno, Wallet, Wallets, WalletsByPublicKeys
from pytonapi.rest.resources._base import BaseResource


class WalletResource(BaseResource):
    """WalletResource resource group."""

    async def ton_connect_proof(
        self,
        body: dict[str, t.Any],
    ) -> t.Any:
        """Account verification and token issuance.

        :param body: Request body.
        :return: dict[str, t.Any]
        """
        path = "/v2/wallet/auth/proof"
        return await self._request(
            method="POST",
            path=path,
            body=body,
        )

    async def get_account_seqno(
        self,
        account_id: str,
    ) -> Seqno:
        """Get account seqno.

        :param account_id: Account ID.
        :return: Seqno
        """
        path = f"/v2/wallet/{account_id}/seqno"
        return await self._request(
            method="GET",
            path=path,
            response_model=Seqno,
        )

    async def get_info(
        self,
        account_id: str,
    ) -> Wallet:
        """Get human-friendly information about a wallet without low-level details.

        :param account_id: Account ID.
        :return: Wallet
        """
        path = f"/v2/wallet/{account_id}"
        return await self._request(
            method="GET",
            path=path,
            response_model=Wallet,
        )

    async def get_wallets_by_public_key(
        self,
        public_key: str,
    ) -> Wallets:
        """Get wallets by public key.

        :param public_key: Public key.
        :return: Wallets
        """
        path = f"/v2/pubkeys/{public_key}/wallets"
        return await self._request(
            method="GET",
            path=path,
            response_model=Wallets,
        )

    async def get_wallets_by_public_key_bulk(
        self,
        body: dict[str, t.Any],
    ) -> WalletsByPublicKeys:
        """Get wallets by a list of public keys.

        :param body: Request body.
        :return: WalletsByPublicKeys
        """
        path = "/v2/pubkeys/wallets/_bulk"
        return await self._request(
            method="POST",
            path=path,
            body=body,
            response_model=WalletsByPublicKeys,
        )

    async def emulate_message_to_wallet(
        self,
        body: dict[str, t.Any],
        currency: str | None = None,
        accept_language: str | None = None,
    ) -> MessageConsequences:
        """Emulate a wallet message on the current blockchain state and derives its consequences for the signing wallet.

        :param body: Request body.
        :param currency: Currency.
        :param accept_language: Accept language.
        :return: MessageConsequences
        """
        path = "/v2/wallet/emulate"
        params = {"currency": currency}
        headers = {"Accept-Language": accept_language}
        return await self._request(
            method="POST",
            path=path,
            params=params,
            body=body,
            headers=headers,
            response_model=MessageConsequences,
        )
