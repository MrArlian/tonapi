# This file is auto-generated. Do not edit manually.

from __future__ import annotations

import typing as t

from pydantic import BaseModel, Field

from pytonapi.rest.models._enums import PoolImplementationType


class AccountStakingInfo(BaseModel):
    pool: str
    amount: int
    pending_deposit: int
    pending_withdraw: int
    ready_withdraw: int


class AccountStaking(BaseModel):
    pools: t.List[AccountStakingInfo]


class ApyHistory(BaseModel):
    apy: float
    time: int


class PoolImplementation(BaseModel):
    name: str
    description: str
    url: str
    socials: t.List[str]


class PoolInfo(BaseModel):
    address: str
    name: str
    total_amount: int
    implementation: PoolImplementationType
    apy: float
    min_stake: int
    cycle_start: int
    cycle_end: int
    verified: bool
    current_nominators: int
    max_nominators: int
    nominators_stake: int
    validator_stake: int
    liquid_jetton_master: t.Optional[str] = Field(default=None)
    cycle_length: t.Optional[int] = Field(default=None)
