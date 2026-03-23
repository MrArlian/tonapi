# This file is auto-generated. Do not edit manually.

from __future__ import annotations

import typing as t

from pytonapi.rest.models import AccountStaking
from pytonapi.rest.resources._base import BaseResource


class StakingResource(BaseResource):
    """StakingResource resource group."""

    async def get_account_nominators_pools(
        self,
        account_id: str,
    ) -> AccountStaking:
        """All pools where account participates.

        :param account_id: Account ID.
        :return: AccountStaking
        """
        path = f"/v2/staking/nominator/{account_id}/pools"
        return await self._request(
            method="GET",
            path=path,
            response_model=AccountStaking,
        )

    async def get_pool_info(
        self,
        account_id: str,
        accept_language: str | None = None,
    ) -> t.Any:
        """Stacking pool info.

        :param account_id: Account ID.
        :param accept_language: Accept language.
        :return: dict[str, t.Any]
        """
        path = f"/v2/staking/pool/{account_id}"
        headers = {"Accept-Language": accept_language}
        return await self._request(
            method="GET",
            path=path,
            headers=headers,
        )

    async def get_pool_history(
        self,
        account_id: str,
        before_lt: int | None = None,
        limit: int = 100,
    ) -> t.Any:
        """Pool history.

        :param account_id: Account ID.
        :param before_lt: Omit this parameter to get last log entries.
        :param limit: Limit.
        :return: dict[str, t.Any]
        """
        path = f"/v2/staking/pool/{account_id}/history"
        params = {
            "before_lt": before_lt,
            "limit": limit,
        }
        return await self._request(
            method="GET",
            path=path,
            params=params,
        )

    async def get_pools(
        self,
        available_for: str | None = None,
        include_unverified: bool | None = None,
        accept_language: str | None = None,
    ) -> t.Any:
        """All pools available in network.

        :param available_for: Account ID.
        :param include_unverified: Return also pools not from white list - just
            compatible by interfaces (maybe dangerous!).
        :param accept_language: Accept language.
        :return: dict[str, t.Any]
        """
        path = "/v2/staking/pools"
        params = {
            "available_for": available_for,
            "include_unverified": include_unverified,
        }
        headers = {"Accept-Language": accept_language}
        return await self._request(
            method="GET",
            path=path,
            params=params,
            headers=headers,
        )
