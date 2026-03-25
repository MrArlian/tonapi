# This file is auto-generated. Do not edit manually.

from __future__ import annotations

import typing as t

from pydantic import BaseModel, Field

if t.TYPE_CHECKING:
    from pytonapi.rest.models.accounts import AccountAddress
    from pytonapi.rest.models.nft import Price


class Metadata(BaseModel):
    encrypted_binary: str
    decryption_key: str | None = Field(default=None)


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
    purchases: list[Purchase]
    next_from: int
