# This file is auto-generated. Do not edit manually.

from __future__ import annotations

import typing as t

from pydantic import BaseModel, Field

ChartPoints = t.List[t.List[float]]


class MarketTonRates(BaseModel):
    market: str
    usd_price: float
    last_date_update: int


class TokenRates(BaseModel):
    prices: t.Optional[t.Dict[str, float]] = Field(default=None)
    diff_24h: t.Optional[t.Dict[str, str]] = Field(default=None)
    diff_7d: t.Optional[t.Dict[str, str]] = Field(default=None)
    diff_30d: t.Optional[t.Dict[str, str]] = Field(default=None)
