# This file is auto-generated. Do not edit manually.

from pytonapi.rest.models import Auctions, DnsRecord, DomainBids, DomainInfo
from tests.conftest import TestTonapiRest
from tests.rest.fixtures import params


class TestDNSResource(TestTonapiRest):
    async def test_get_info(self):
        p = params("dns.get_info")
        response = await self.tonapi.dns.get_info(
            p["domain_name"],
        )
        self.assertIsInstance(response, DomainInfo)

    async def test_resolve(self):
        p = params("dns.resolve")
        response = await self.tonapi.dns.resolve(
            p["domain_name"],
        )
        self.assertIsInstance(response, DnsRecord)

    async def test_get_domain_bids(self):
        p = params("dns.get_domain_bids")
        response = await self.tonapi.dns.get_domain_bids(
            p["domain_name"],
        )
        self.assertIsInstance(response, DomainBids)

    async def test_get_all_auctions(self):
        response = await self.tonapi.dns.get_all_auctions()
        self.assertIsInstance(response, Auctions)
