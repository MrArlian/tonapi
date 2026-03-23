# This file is auto-generated. Do not edit manually.

from __future__ import annotations

import typing as t

from pydantic import BaseModel, Field

if t.TYPE_CHECKING:
    from pytonapi.rest.models.accounts import AccountAddress, JettonPreview
    from pytonapi.rest.models.nft import NftItem


class JettonQuantity(BaseModel):
    quantity: str
    wallet_address: AccountAddress
    jetton: JettonPreview


class Risk(BaseModel):
    transfer_all_remaining_balance: bool
    ton: int
    jettons: list[JettonQuantity]
    nfts: list[NftItem]
    total_equivalent: float | None = Field(default=None)


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
