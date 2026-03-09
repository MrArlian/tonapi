# This file is auto-generated. Do not edit manually.

from __future__ import annotations

from pydantic import BaseModel


class BlockRaw(BaseModel):
    workchain: int
    shard: str
    seqno: int
    root_hash: str
    file_hash: str


class InitStateRaw(BaseModel):
    workchain: int
    root_hash: str
    file_hash: str
