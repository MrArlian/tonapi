# This file is auto-generated. Do not edit manually.

from __future__ import annotations

from pydantic import BaseModel, Field

from pytonapi.rest.models._enums import AccountStatus


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
    plugins: list[WalletPlugin]
    status: AccountStatus
    last_activity: int
    get_methods: list[str]
    last_lt: int
    name: str | None = Field(default=None)
    icon: str | None = Field(default=None)
    is_suspended: bool | None = Field(default=None)
    signature_disabled: bool | None = Field(default=None)
    interfaces: list[str] | None = Field(default=None)


class Wallets(BaseModel):
    accounts: list[Wallet]


class WalletsByPublicKey(BaseModel):
    public_key: str
    wallets: list[Wallet]


class WalletsByPublicKeys(BaseModel):
    items: list[WalletsByPublicKey]
