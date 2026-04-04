# This file is auto-generated. Do not edit manually.

from __future__ import annotations

import typing as t

from pydantic import BaseModel, ConfigDict, Field

if t.TYPE_CHECKING:
    from pytonapi.rest.models.accounts import AccountAddress
    from pytonapi.rest.models.nft import NftItem


class Auction(BaseModel):
    domain: str
    owner: str
    price: int
    bids: int
    date: int


class Auctions(BaseModel):
    data: list[Auction]
    total: int


class PictureDNS(BaseModel):
    type: str
    url: str | None = Field(default=None)
    bag_id: str | None = Field(default=None)


class WalletDNS(BaseModel):
    address: str
    account: AccountAddress
    is_wallet: bool
    has_method_pubkey: bool
    has_method_seqno: bool
    names: list[str]


class DnsRecord(BaseModel):
    sites: list[str]
    wallet: WalletDNS | None = Field(default=None)
    next_resolver: str | None = Field(default=None)
    storage: str | None = Field(default=None)
    picture: PictureDNS | None = Field(default=None)


class DomainBid(BaseModel):
    success: bool
    value: int
    tx_time: int = Field(alias="txTime")
    tx_hash: str = Field(alias="txHash")
    bidder: AccountAddress

    model_config = ConfigDict(populate_by_name=True)


class DomainBids(BaseModel):
    data: list[DomainBid]


class DomainInfo(BaseModel):
    name: str
    expiring_at: int | None = Field(default=None)
    item: NftItem | None = Field(default=None)
