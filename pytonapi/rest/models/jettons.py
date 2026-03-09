# This file is auto-generated. Do not edit manually.

from __future__ import annotations

import typing as t

from pydantic import BaseModel, Field

from pytonapi.rest.models._enums import JettonVerificationType

if t.TYPE_CHECKING:
    from pytonapi.rest.models.accounts import AccountAddress


class JettonHolders(BaseModel):
    addresses: t.List[t.Any]
    total: int


class ScaledUI(BaseModel):
    numerator: str
    denominator: str


class JettonMetadata(BaseModel):
    address: str
    name: str
    symbol: str
    decimals: str
    image: t.Optional[str] = Field(default=None)
    description: t.Optional[str] = Field(default=None)
    social: t.Optional[t.List[str]] = Field(default=None)
    websites: t.Optional[t.List[str]] = Field(default=None)
    catalogs: t.Optional[t.List[str]] = Field(default=None)
    custom_payload_api_uri: t.Optional[str] = Field(default=None)


class JettonInfo(BaseModel):
    mintable: bool
    total_supply: str
    metadata: JettonMetadata
    preview: str
    verification: JettonVerificationType
    holders_count: int
    admin: t.Optional[AccountAddress] = Field(default=None)
    scaled_ui: t.Optional[ScaledUI] = Field(default=None)


class JettonTransferPayload(BaseModel):
    custom_payload: t.Optional[str] = Field(default=None)
    state_init: t.Optional[str] = Field(default=None)


class Jettons(BaseModel):
    jettons: t.List[JettonInfo]
