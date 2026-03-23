# This file is auto-generated. Do not edit manually.

from __future__ import annotations

from pydantic import BaseModel, Field

ChartPoints = list[list[float]]


class MarketTonRates(BaseModel):
    market: str
    usd_price: float
    last_date_update: int


class TokenRates(BaseModel):
    prices: dict[str, float] | None = Field(default=None)
    diff_24h: dict[str, str] | None = Field(default=None)
    diff_7d: dict[str, str] | None = Field(default=None)
    diff_30d: dict[str, str] | None = Field(default=None)
