# This file is auto-generated. Do not edit manually.

from __future__ import annotations

import typing as t

from pytonapi.rest.models import AccountPurchases
from pytonapi.rest.resources._base import BaseResource


class PurchasesResource(BaseResource):
    async def get_purchase_history(
        self,
        account_id: str,
        before_lt: t.Optional[int] = None,
        limit: int = 100,
    ) -> AccountPurchases:
        """
        Get history of purchases.

        :param account_id: Account ID.
        :param before_lt: Omit this parameter to get last invoices.
        :param limit: Limit.
        :return: AccountPurchases
        """
        path = f"/v2/purchases/{account_id}/history"
        params = {
            "before_lt": before_lt,
            "limit": limit,
        }
        return await self._request(
            method="GET",
            path=path,
            params=params,
            response_model=AccountPurchases,
        )
