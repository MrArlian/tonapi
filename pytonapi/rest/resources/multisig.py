# This file is auto-generated. Do not edit manually.

from __future__ import annotations

from pytonapi.rest.models import Multisig, MultisigOrder
from pytonapi.rest.resources._base import BaseResource


class MultisigResource(BaseResource):
    """MultisigResource resource group."""

    async def get_account(
        self,
        account_id: str,
    ) -> Multisig:
        """Get multisig account info.

        :param account_id: Account ID.
        :return: Multisig
        """
        path = f"/v2/multisig/{account_id}"
        return await self._request(
            method="GET",
            path=path,
            response_model=Multisig,
        )

    async def get_order(
        self,
        account_id: str,
    ) -> MultisigOrder:
        """Get multisig order.

        :param account_id: Account ID.
        :return: MultisigOrder
        """
        path = f"/v2/multisig/order/{account_id}"
        return await self._request(
            method="GET",
            path=path,
            response_model=MultisigOrder,
        )
