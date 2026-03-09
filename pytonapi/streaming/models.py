import typing as t

from pydantic import BaseModel, Field


class BlockEvent(BaseModel):
    """New block notification."""

    workchain: int
    shard: str
    seqno: int
    root_hash: str
    file_hash: str


class TransactionEvent(BaseModel):
    """Finalized transaction notification."""

    account_id: str
    lt: int
    tx_hash: str


class TraceEvent(BaseModel):
    """Completed trace notification."""

    accounts: t.List[str]
    hash: str


class MempoolEvent(BaseModel):
    """Pending inbound message notification."""

    boc: str
    involved_accounts: t.Optional[t.List[str]] = Field(default=None)
