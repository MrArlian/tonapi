# This file is auto-generated. Do not edit manually.

from __future__ import annotations

import typing as t

from pydantic import BaseModel, Field

if t.TYPE_CHECKING:
    from pytonapi.rest.models.blockchain import Transaction


class Trace(BaseModel):
    transaction: Transaction
    interfaces: list[str]
    children: list[Trace] | None = Field(default=None)
    emulated: bool | None = Field(default=None)
