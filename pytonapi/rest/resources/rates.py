# This file is auto-generated. Do not edit manually.

from __future__ import annotations

import typing as t

from pytonapi.rest.resources._base import BaseResource


class RatesResource(BaseResource):
    async def get_rates(
        self,
        tokens: t.List[str],
        currencies: t.List[str],
    ) -> t.Dict[str, t.Any]:
        """
        Get the token price in the chosen currency for display only. Don’t use this for
        financial transactions.

        :param tokens: Accept ton and jetton master addresses, separated by commas.
        :param currencies: Accept ton and all possible fiat currencies, separated by
            commas.
        :return: t.Dict[str, t.Any]
        """
        path = "/v2/rates"
        params = {
            "tokens": tokens,
            "currencies": currencies,
        }
        return await self._request(
            method="GET",
            path=path,
            params=params,
        )

    async def get_chart_rates(
        self,
        token: str,
        currency: t.Optional[str] = None,
        start_date: t.Optional[int] = None,
        end_date: t.Optional[int] = None,
        points_count: int = 200,
    ) -> t.Dict[str, t.Any]:
        """
        Get chart by token.

        :param token: Accept jetton master address.
        :param currency: Currency.
        :param start_date: Start date.
        :param end_date: End date.
        :param points_count: Points count.
        :return: t.Dict[str, t.Any]
        """
        path = "/v2/rates/chart"
        params = {
            "token": token,
            "currency": currency,
            "start_date": start_date,
            "end_date": end_date,
            "points_count": points_count,
        }
        return await self._request(
            method="GET",
            path=path,
            params=params,
        )

    async def get_markets_rates(
        self,
    ) -> t.Dict[str, t.Any]:
        """
        Get the TON price from markets.

        :return: t.Dict[str, t.Any]
        """
        path = "/v2/rates/markets"
        return await self._request(
            method="GET",
            path=path,
        )
