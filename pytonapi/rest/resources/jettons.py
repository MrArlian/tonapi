# This file is auto-generated. Do not edit manually.

from __future__ import annotations

import typing as t

from pytonapi.rest.models import Event, JettonHolders, JettonInfo, Jettons, JettonTransferPayload
from pytonapi.rest.resources._base import BaseResource


class JettonsResource(BaseResource):
    """JettonsResource resource group."""

    async def get_jettons(
        self,
        limit: int = 100,
        offset: int = 0,
    ) -> Jettons:
        """Get a list of all indexed jetton masters in the blockchain.

        :param limit: Limit.
        :param offset: Offset.
        :return: Jettons
        """
        path = "/v2/jettons"
        params = {
            "limit": limit,
            "offset": offset,
        }
        return await self._request(
            method="GET",
            path=path,
            params=params,
            response_model=Jettons,
        )

    async def get_jetton_info(
        self,
        account_id: str,
    ) -> JettonInfo:
        """Get jetton metadata by jetton master address.

        :param account_id: Account ID.
        :return: JettonInfo
        """
        path = f"/v2/jettons/{account_id}"
        return await self._request(
            method="GET",
            path=path,
            response_model=JettonInfo,
        )

    async def get_jetton_infos_by_addresses(
        self,
        body: dict[str, t.Any],
    ) -> Jettons:
        """Get jetton metadata items by jetton master addresses.

        :param body: Request body.
        :return: Jettons
        """
        path = "/v2/jettons/_bulk"
        return await self._request(
            method="POST",
            path=path,
            body=body,
            response_model=Jettons,
        )

    async def get_jetton_holders(
        self,
        account_id: str,
        limit: int = 1000,
        offset: int = 0,
    ) -> JettonHolders:
        """Get jetton's holders.

        :param account_id: Account ID.
        :param limit: Limit.
        :param offset: Offset.
        :return: JettonHolders
        """
        path = f"/v2/jettons/{account_id}/holders"
        params = {
            "limit": limit,
            "offset": offset,
        }
        return await self._request(
            method="GET",
            path=path,
            params=params,
            response_model=JettonHolders,
        )

    async def get_jetton_transfer_payload(
        self,
        account_id: str,
        jetton_id: str,
    ) -> JettonTransferPayload:
        """Get jetton's custom payload and state init required for transfer.

        :param account_id: Account ID.
        :param jetton_id: Jetton ID.
        :return: JettonTransferPayload
        """
        path = f"/v2/jettons/{jetton_id}/transfer/{account_id}/payload"
        return await self._request(
            method="GET",
            path=path,
            response_model=JettonTransferPayload,
        )

    async def get_events(
        self,
        event_id: str,
        accept_language: str | None = None,
    ) -> Event:
        """Get only jetton transfers in the event.

        :param event_id: Event ID or transaction hash in hex (without 0x) or base64url
            format.
        :param accept_language: Accept language.
        :return: Event
        """
        path = f"/v2/events/{event_id}/jettons"
        headers = {"Accept-Language": accept_language}
        return await self._request(
            method="GET",
            path=path,
            headers=headers,
            response_model=Event,
        )
