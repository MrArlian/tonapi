# This file is auto-generated. Do not edit manually.

from __future__ import annotations

import typing as t

from pytonapi.rest.resources._base import BaseResource


class StorageResource(BaseResource):
    """StorageResource resource group."""

    async def get_providers(
        self,
    ) -> t.Any:
        """Get TON storage providers deployed to the blockchain.

        :return: dict[str, t.Any]
        """
        path = "/v2/storage/providers"
        return await self._request(
            method="GET",
            path=path,
        )
