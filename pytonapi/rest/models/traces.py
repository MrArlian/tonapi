# This file is auto-generated. Do not edit manually.

from __future__ import annotations

import typing as t

from pydantic import BaseModel, Field

if t.TYPE_CHECKING:
    from pytonapi.rest.models.blockchain import Transaction


class Trace(BaseModel):
    transaction: Transaction
    interfaces: t.List[str]
    children: t.Optional[t.List[Trace]] = Field(default=None)
    emulated: t.Optional[bool] = Field(default=None)
