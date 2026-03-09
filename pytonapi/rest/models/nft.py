# This file is auto-generated. Do not edit manually.

from __future__ import annotations

import typing as t

from pydantic import BaseModel, Field

from pytonapi.rest.models._enums import TrustType

if t.TYPE_CHECKING:
    from pytonapi.rest.models.accounts import AccountAddress
    from pytonapi.rest.models.purchases import Price

NftApprovedBy = t.List[str]


class ImagePreview(BaseModel):
    resolution: str
    url: str


class NftCollection(BaseModel):
    address: str
    next_item_index: int
    raw_collection_content: str
    approved_by: NftApprovedBy
    owner: t.Optional[AccountAddress] = Field(default=None)
    metadata: t.Optional[t.Dict[str, t.Any]] = Field(default=None)
    previews: t.Optional[t.List[ImagePreview]] = Field(default=None)


class NftCollections(BaseModel):
    nft_collections: t.List[NftCollection]


class Sale(BaseModel):
    address: str
    market: AccountAddress
    price: Price
    owner: t.Optional[AccountAddress] = Field(default=None)


class NftItem(BaseModel):
    address: str
    index: int
    verified: bool
    metadata: t.Dict[str, t.Any]
    approved_by: NftApprovedBy
    trust: TrustType
    owner: t.Optional[AccountAddress] = Field(default=None)
    collection: t.Optional[t.Any] = Field(default=None)
    sale: t.Optional[Sale] = Field(default=None)
    previews: t.Optional[t.List[ImagePreview]] = Field(default=None)
    dns: t.Optional[str] = Field(default=None)
    include_cnft: t.Optional[bool] = Field(default=None)


class NftItems(BaseModel):
    nft_items: t.List[NftItem]


class NftOperation(BaseModel):
    operation: str
    utime: int
    lt: int
    transaction_hash: str
    item: NftItem
    source: t.Optional[AccountAddress] = Field(default=None)
    destination: t.Optional[AccountAddress] = Field(default=None)


class NftOperations(BaseModel):
    operations: t.List[NftOperation]
    next_from: t.Optional[int] = Field(default=None)
