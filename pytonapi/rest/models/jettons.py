# This file is auto-generated. Do not edit manually.

from __future__ import annotations

import typing as t

from pydantic import BaseModel, Field

from pytonapi.rest.models._enums import JettonVerificationType

if t.TYPE_CHECKING:
    from pytonapi.rest.models.accounts import AccountAddress


class JettonHolders(BaseModel):
    addresses: list[t.Any]
    total: int


class JettonMetadata(BaseModel):
    address: str
    name: str
    symbol: str
    decimals: str
    image: str | None = Field(default=None)
    description: str | None = Field(default=None)
    social: list[str] | None = Field(default=None)
    websites: list[str] | None = Field(default=None)
    catalogs: list[str] | None = Field(default=None)
    custom_payload_api_uri: str | None = Field(default=None)


class ScaledUI(BaseModel):
    numerator: str
    denominator: str


class JettonInfo(BaseModel):
    mintable: bool
    total_supply: str
    metadata: JettonMetadata
    preview: str
    verification: JettonVerificationType
    holders_count: int
    admin: AccountAddress | None = Field(default=None)
    scaled_ui: ScaledUI | None = Field(default=None)
    code_hash: str | None = Field(default=None)
    data_hash: str | None = Field(default=None)
    last_transaction_lt: str | None = Field(default=None)
    name: str | None = Field(default=None)
    interfaces: list[str] | None = Field(default=None)


class JettonTransferPayload(BaseModel):
    custom_payload: str | None = Field(default=None)
    state_init: str | None = Field(default=None)


class Jettons(BaseModel):
    jettons: list[JettonInfo]
