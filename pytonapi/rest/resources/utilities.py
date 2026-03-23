# This file is auto-generated. Do not edit manually.

from __future__ import annotations

import typing as t

from pytonapi.rest.models import ServiceStatus
from pytonapi.rest.resources._base import BaseResource


class UtilitiesResource(BaseResource):
    """UtilitiesResource resource group."""

    async def get_openapi_json(
        self,
    ) -> t.Any:
        """Get the openapi.json file.

        :return: dict[str, t.Any]
        """
        path = "/v2/openapi.json"
        return await self._request(
            method="GET",
            path=path,
        )

    async def get_openapi_yml(
        self,
    ) -> str:
        """Get the openapi.yml file.

        :return: str
        """
        path = "/v2/openapi.yml"
        return await self._request(
            method="GET",
            path=path,
            response_model=str,
        )

    async def status(
        self,
    ) -> ServiceStatus:
        """Status.

        :return: ServiceStatus
        """
        path = "/v2/status"
        return await self._request(
            method="GET",
            path=path,
            response_model=ServiceStatus,
        )

    async def address_parse(
        self,
        account_id: str,
    ) -> t.Any:
        """parse address and display in all formats.

        :param account_id: Account ID.
        :return: dict[str, t.Any]
        """
        path = f"/v2/address/{account_id}/parse"
        return await self._request(
            method="GET",
            path=path,
        )
