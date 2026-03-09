# This file is auto-generated. Do not edit manually.

from __future__ import annotations

import typing as t

from pydantic import BaseModel, Field

from pytonapi.rest.models._enums import CurrencyType, TrustType

if t.TYPE_CHECKING:
    from pytonapi.rest.models.accounts import AccountAddress


class Metadata(BaseModel):
    encrypted_binary: str
    decryption_key: t.Optional[str] = Field(default=None)


class Price(BaseModel):
    currency_type: CurrencyType
    value: str
    decimals: int
    token_name: str
    verification: TrustType
    image: str
    jetton: t.Optional[str] = Field(default=None)


class Purchase(BaseModel):
    event_id: str
    invoice_id: str
    source: AccountAddress
    destination: AccountAddress
    lt: int
    utime: int
    amount: Price
    metadata: Metadata


class AccountPurchases(BaseModel):
    purchases: t.List[Purchase]
    next_from: int
