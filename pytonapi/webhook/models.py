import enum
import typing as t

from pydantic import BaseModel


class WebhookEventType(str, enum.Enum):
    """Webhook event type identifier."""

    ACCOUNT_TX = "account_tx"
    MEMPOOL_MSG = "mempool_msg"
    OPCODE_MSG = "opcode_msg"
    NEW_CONTRACTS = "new_contracts"


class AccountTxEvent(BaseModel):
    """Account transaction event."""

    event_type: t.Literal["account_tx"] = "account_tx"
    account_id: str
    lt: int
    tx_hash: str


class MempoolMsgEvent(BaseModel):
    """Mempool message event."""

    event_type: t.Literal["mempool_msg"] = "mempool_msg"
    boc: str


class OpcodeMsgEvent(BaseModel):
    """Opcode subscription event."""

    event_type: t.Literal["opcode_msg"] = "opcode_msg"
    account_id: str
    lt: int
    tx_hash: str


class NewContractsEvent(BaseModel):
    """New contract deployment event."""

    event_type: t.Literal["new_contracts"] = "new_contracts"
    account_id: str
    lt: int
    tx_hash: str


class AccountSubscription(BaseModel):
    """Account transaction subscription details."""

    account_id: str
    last_delivered_lt: int
    failed_at: t.Optional[str] = None
    failed_lt: t.Optional[int] = None
    failed_attempts: t.Optional[int] = None


class WebhookInfo(BaseModel):
    """Webhook metadata returned by the API."""

    id: int
    endpoint: str
    token: str
    subscribed_accounts: int
    subscribed_msg_opcodes: int
    subscribed_to_mempool: bool
    subscribed_to_new_contracts: bool
    status: str
    status_updated_at: str
    last_online_at: str
    status_failed_attempts: int
