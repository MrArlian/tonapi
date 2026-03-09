# This file is auto-generated. Do not edit manually.

from __future__ import annotations

import typing as t

from pydantic import BaseModel, Field

if t.TYPE_CHECKING:
    from pytonapi.rest.models.accounts import AccountAddress, Action


class ValueFlow(BaseModel):
    account: AccountAddress
    ton: int
    fees: int
    jettons: t.Optional[t.List[t.Any]] = Field(default=None)


class Event(BaseModel):
    event_id: str
    timestamp: int
    actions: t.List[Action]
    value_flow: t.List[ValueFlow]
    is_scam: bool
    lt: int
    in_progress: bool
    progress: float
    last_slice_id: t.Optional[int] = Field(default=None)
    ext_msg_hash: t.Optional[str] = Field(default=None)
