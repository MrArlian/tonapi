# This file is auto-generated. Do not edit manually.

from __future__ import annotations

import typing as t

from pydantic import BaseModel, Field

if t.TYPE_CHECKING:
    from pytonapi.rest.models.accounts import AccountAddress


class DecodedMessage(BaseModel):
    destination: AccountAddress
    destination_wallet_version: str
    ext_in_msg_decoded: t.Optional[t.Any] = Field(default=None)


class DecodedRawMessage(BaseModel):
    message: t.Any
    mode: int
