# This file is auto-generated. Do not edit manually.

from __future__ import annotations

from pytonapi.rest.models import EcPreview
from pytonapi.rest.resources._base import BaseResource


class ExtraCurrencyResource(BaseResource):
    async def get_info(
        self,
        id: int,
    ) -> EcPreview:
        """
        Get extra currency info by id.

        :param id: Extra currency id.
        :return: EcPreview
        """
        path = f"/v2/extra-currency/{id}"
        return await self._request(
            method="GET",
            path=path,
            response_model=EcPreview,
        )
