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
    data: t.List[Auction]
    total: int


class PictureDNS(BaseModel):
    type: str
    url: t.Optional[str] = Field(default=None)
    bag_id: t.Optional[str] = Field(default=None)


class WalletDNS(BaseModel):
    address: str
    account: AccountAddress
    is_wallet: bool
    has_method_pubkey: bool
    has_method_seqno: bool
    names: t.List[str]


class DnsRecord(BaseModel):
    sites: t.List[str]
    wallet: t.Optional[WalletDNS] = Field(default=None)
    next_resolver: t.Optional[str] = Field(default=None)
    storage: t.Optional[str] = Field(default=None)
    picture: t.Optional[PictureDNS] = Field(default=None)


class DomainBid(BaseModel):
    success: bool
    value: int
    tx_time: int = Field(alias="txTime")
    tx_hash: str = Field(alias="txHash")
    bidder: AccountAddress

    model_config = ConfigDict(populate_by_name=True)


class DomainBids(BaseModel):
    data: t.List[DomainBid]


class DomainInfo(BaseModel):
    name: str
    expiring_at: t.Optional[int] = Field(default=None)
    item: t.Optional[NftItem] = Field(default=None)
