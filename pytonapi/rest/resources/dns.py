# This file is auto-generated. Do not edit manually.

from __future__ import annotations

import typing as t

from pytonapi.rest.models import Auctions, DnsRecord, DomainBids, DomainInfo
from pytonapi.rest.resources._base import BaseResource


class DNSResource(BaseResource):
    async def get_info(
        self,
        domain_name: str,
    ) -> DomainInfo:
        """
        Get full information about domain name.

        :param domain_name: Domain name with .ton or .t.me.
        :return: DomainInfo
        """
        path = f"/v2/dns/{domain_name}"
        return await self._request(
            method="GET",
            path=path,
            response_model=DomainInfo,
        )

    async def resolve(
        self,
        domain_name: str,
        filter: bool = False,
    ) -> DnsRecord:
        """
        DNS resolve for domain name.

        :param domain_name: Domain name with .ton or .t.me.
        :param filter: Filter.
        :return: DnsRecord
        """
        path = f"/v2/dns/{domain_name}/resolve"
        params = {"filter": filter}
        return await self._request(
            method="GET",
            path=path,
            params=params,
            response_model=DnsRecord,
        )

    async def get_domain_bids(
        self,
        domain_name: str,
    ) -> DomainBids:
        """
        Get domain bids.

        :param domain_name: Domain name with .ton or .t.me.
        :return: DomainBids
        """
        path = f"/v2/dns/{domain_name}/bids"
        return await self._request(
            method="GET",
            path=path,
            response_model=DomainBids,
        )

    async def get_all_auctions(
        self,
        tld: t.Optional[str] = None,
    ) -> Auctions:
        """
        Get all auctions.

        :param tld: Domain filter for current auctions "ton" or "t.me".
        :return: Auctions
        """
        path = "/v2/dns/auctions"
        params = {"tld": tld}
        return await self._request(
            method="GET",
            path=path,
            params=params,
            response_model=Auctions,
        )
