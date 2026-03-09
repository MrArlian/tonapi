# This file is auto-generated. Do not edit manually.

from __future__ import annotations

import typing as t

from pytonapi.rest.resources._base import BaseResource


class StorageResource(BaseResource):
    async def get_providers(
        self,
    ) -> t.Dict[str, t.Any]:
        """
        Get TON storage providers deployed to the blockchain.

        :return: t.Dict[str, t.Any]
        """
        path = "/v2/storage/providers"
        return await self._request(
            method="GET",
            path=path,
        )
