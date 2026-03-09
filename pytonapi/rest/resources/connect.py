# This file is auto-generated. Do not edit manually.

from __future__ import annotations

import typing as t

from pytonapi.rest.models import AccountInfoByStateInit
from pytonapi.rest.resources._base import BaseResource


class ConnectResource(BaseResource):
    async def get_ton_connect_payload(
        self,
    ) -> t.Dict[str, t.Any]:
        """
        Get a payload for further token receipt.

        :return: t.Dict[str, t.Any]
        """
        path = "/v2/tonconnect/payload"
        return await self._request(
            method="GET",
            path=path,
        )

    async def get_account_info_by_state_init(
        self,
        body: t.Dict[str, t.Any],
    ) -> AccountInfoByStateInit:
        """
        Get account info by state init.

        :param body: Request body.
        :return: AccountInfoByStateInit
        """
        path = "/v2/tonconnect/stateinit"
        return await self._request(
            method="POST",
            path=path,
            body=body,
            response_model=AccountInfoByStateInit,
        )
