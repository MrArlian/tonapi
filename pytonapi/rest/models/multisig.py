# This file is auto-generated. Do not edit manually.

from __future__ import annotations

import typing as t

from pydantic import BaseModel, Field

if t.TYPE_CHECKING:
    from pytonapi.rest.models.emulation import Risk


class MultisigOrder(BaseModel):
    address: str
    order_seqno: str
    threshold: int
    sent_for_execution: bool
    signers: list[str]
    approvals_num: int
    expiration_date: int
    risk: Risk
    creation_date: int
    signed_by: list[str]
    multisig_address: str
    changing_parameters: t.Any | None = Field(default=None)


class Multisig(BaseModel):
    address: str
    seqno: str
    threshold: int
    signers: list[str]
    proposers: list[str]
    orders: list[MultisigOrder]
