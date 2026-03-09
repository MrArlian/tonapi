# This file is auto-generated. Do not edit manually.

from __future__ import annotations

import typing as t

from pydantic import BaseModel, Field

from pytonapi.rest.models._enums import AccountStatus

if t.TYPE_CHECKING:
    from pytonapi.rest.models.accounts import AccountEvent
    from pytonapi.rest.models.multisig import Risk
    from pytonapi.rest.models.traces import Trace


class MessageConsequences(BaseModel):
    trace: Trace
    risk: Risk
    event: AccountEvent


class Seqno(BaseModel):
    seqno: int


class WalletPlugin(BaseModel):
    address: str
    type: str
    status: AccountStatus


class WalletStats(BaseModel):
    nfts_count: int
    jettons_count: int
    multisig_count: int
    staking_count: int


class Wallet(BaseModel):
    address: str
    is_wallet: bool
    balance: int
    stats: WalletStats
    plugins: t.List[WalletPlugin]
    status: AccountStatus
    last_activity: int
    get_methods: t.List[str]
    last_lt: int
    name: t.Optional[str] = Field(default=None)
    icon: t.Optional[str] = Field(default=None)
    is_suspended: t.Optional[bool] = Field(default=None)
    signature_disabled: t.Optional[bool] = Field(default=None)
    interfaces: t.Optional[t.List[str]] = Field(default=None)


class Wallets(BaseModel):
    accounts: t.List[Wallet]


class WalletsByPublicKey(BaseModel):
    public_key: str
    wallets: t.List[Wallet]


class WalletsByPublicKeys(BaseModel):
    items: t.List[WalletsByPublicKey]
