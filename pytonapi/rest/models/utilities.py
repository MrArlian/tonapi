# This file is auto-generated. Do not edit manually.

from __future__ import annotations

from pydantic import BaseModel


class ServiceStatus(BaseModel):
    rest_online: bool
    indexing_latency: int
    last_known_masterchain_seqno: int
