# This file is auto-generated. Do not edit manually.

from __future__ import annotations

from pydantic import BaseModel, Field

from pytonapi.rest.models._enums import PoolImplementationType


class AccountStakingInfo(BaseModel):
    pool: str
    amount: int
    pending_deposit: int
    pending_withdraw: int
    ready_withdraw: int


class AccountStaking(BaseModel):
    pools: list[AccountStakingInfo]


class ApyHistory(BaseModel):
    apy: float
    time: int


class PoolImplementation(BaseModel):
    name: str
    description: str
    url: str
    socials: list[str]


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
    liquid_jetton_master: str | None = Field(default=None)
    cycle_length: int | None = Field(default=None)
