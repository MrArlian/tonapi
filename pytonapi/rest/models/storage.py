# This file is auto-generated. Do not edit manually.

from __future__ import annotations

from pydantic import BaseModel


class StorageProvider(BaseModel):
    address: str
    accept_new_contracts: bool
    rate_per_mb_day: int
    max_span: int
    minimal_file_size: int
    maximal_file_size: int
