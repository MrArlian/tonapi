# This file is auto-generated. Do not edit manually.

from __future__ import annotations

import typing as t

from pytonapi.rest.models import GaslessConfig, GaslessTx, SignRawParams
from pytonapi.rest.resources._base import BaseResource


class GaslessResource(BaseResource):
    async def config(
        self,
    ) -> GaslessConfig:
        """
        Returns configuration of gasless transfers.

        :return: GaslessConfig
        """
        path = "/v2/gasless/config"
        return await self._request(
            method="GET",
            path=path,
            response_model=GaslessConfig,
        )

    async def estimate(
        self,
        master_id: str,
        body: t.Dict[str, t.Any],
        accept_language: t.Optional[str] = None,
    ) -> SignRawParams:
        """
        Estimates the cost of the given messages and returns a payload to sign.

        :param master_id: Jetton to pay commission.
        :param body: Request body.
        :param accept_language: Accept language.
        :return: SignRawParams
        """
        path = f"/v2/gasless/estimate/{master_id}"
        headers = {"Accept-Language": accept_language}
        return await self._request(
            method="POST",
            path=path,
            body=body,
            headers=headers,
            response_model=SignRawParams,
        )

    async def send(
        self,
        body: t.Dict[str, t.Any],
    ) -> GaslessTx:
        """
        Submits the signed gasless transaction message to the network.

        :param body: Request body.
        :return: GaslessTx
        """
        path = "/v2/gasless/send"
        return await self._request(
            method="POST",
            path=path,
            body=body,
            response_model=GaslessTx,
        )
