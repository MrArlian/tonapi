import typing as t
from dataclasses import dataclass, field
from enum import Enum

__all__ = [
    "DEFAULT_RECONNECT_POLICY",
    "DEFAULT_RETRY_POLICY",
    "NETWORK_BASE_URLS",
    "WEBHOOK_BASE_URLS",
    "Network",
    "Opcode",
    "ReconnectPolicy",
    "RetryPolicy",
    "RetryRule",
    "Workchain",
]


class Network(int, Enum):
    """Available TONAPI network environments."""

    MAINNET = -239
    TESTNET = -3
    TETRA = 662387


class Workchain(int, Enum):
    """TON blockchain workchain identifiers."""

    MASTERCHAIN = -1
    BASECHAIN = 0


class Opcode(str, Enum):
    """Well-known TON message operation codes.

    Values are hex strings suitable for use as streaming ``operations``
    filters and webhook ``opcodes`` subscriptions.

    Reference: https://github.com/tonkeeper/tongo/blob/master/abi/messages.md
    """

    # General
    TEXT_COMMENT = "0x00000000"
    ENCRYPTED_TEXT_COMMENT = "0x2167da4b"
    EXCESS = "0xd53276db"
    BOUNCE = "0xffffffff"
    TOP_UP = "0xd372158c"

    # Jetton
    JETTON_TRANSFER = "0x0f8a7ea5"
    JETTON_INTERNAL_TRANSFER = "0x178d4519"
    JETTON_NOTIFY = "0x7362d09c"
    JETTON_BURN = "0x595f07bc"
    JETTON_MINT = "0x642b7d07"
    JETTON_CHANGE_ADMIN = "0x6501f354"
    JETTON_CHANGE_METADATA = "0xcb862902"
    JETTON_CLAIM_ADMIN = "0xfb88e119"
    JETTON_BURN_NOTIFICATION = "0x7bdd97de"
    JETTON_CALL_TO = "0x235caf52"
    JETTON_SET_STATUS = "0xeed236d3"
    JETTON_UPGRADE = "0x2508d66a"

    # NFT
    NFT_TRANSFER = "0x5fcc3d14"
    NFT_OWNERSHIP_ASSIGNED = "0x05138d91"
    GET_ROYALTY_PARAMS = "0x693d3950"
    GET_STATIC_DATA = "0x2fcb26a2"
    REPORT_ROYALTY_PARAMS = "0xa8cb00ad"
    REPORT_STATIC_DATA = "0x8b771735"
    OUTBID_NOTIFICATION = "0x557cea20"
    PROVE_OWNERSHIP = "0x04ded148"
    OWNERSHIP_PROOF = "0x0524c7ae"

    # SBT
    SBT_DESTROY = "0x1f04537a"
    SBT_REVOKE = "0x6f89f5e3"
    SBT_REQUEST_OWNER = "0xd0c3bfea"
    SBT_OWNER_INFO = "0x0dd607e3"

    # DNS
    CHANGE_DNS_RECORD = "0x4eb1f0f9"
    DELETE_DNS_RECORD = CHANGE_DNS_RECORD
    DNS_BALANCE_RELEASE = "0x4ed14b65"

    # Teleitem / Telemint
    TELEITEM_BID_INFO = "0x38127de1"
    TELEITEM_CANCEL_AUCTION = "0x371638ae"
    TELEITEM_DEPLOY = "0x299a3e15"
    TELEITEM_OK = "0xa37a0983"
    TELEITEM_RETURN_BID = "0xa43227e1"
    TELEITEM_START_AUCTION = "0x487a8e81"
    TELEMINT_DEPLOY = "0x4637289a"
    TELEMINT_DEPLOY_V2 = "0x4637289b"

    # Multisig
    MULTISIG_NEW_ORDER = "0xf718510f"
    MULTISIG_APPROVE = "0xa762230f"
    MULTISIG_EXECUTE_INTERNAL = "0xa32c59bf"


NETWORK_BASE_URLS: t.Final[t.Dict[Network, str]] = {
    Network.MAINNET: "https://tonapi.io",
    Network.TESTNET: "https://testnet.tonapi.io",
    Network.TETRA: "https://tetra.tonapi.io",
}

WEBHOOK_BASE_URLS: t.Final[t.Dict[Network, str]] = {
    Network.MAINNET: "https://rt.tonapi.io",
    Network.TESTNET: "https://rt-testnet.tonapi.io",
}


@dataclass(slots=True, frozen=True)
class RetryRule:
    """Single retry rule matching specific HTTP status codes.

    Attributes:
        statuses: HTTP status codes that trigger this rule.
        max_retries: maximum number of retries for these statuses.
        base_delay: initial delay in seconds before first retry.
        max_delay: upper bound for the delay after backoff.
        backoff_factor: multiplier applied to delay on each retry.
    """

    statuses: t.FrozenSet[int]
    max_retries: int = 3
    base_delay: float = 1.0
    max_delay: float = 30.0
    backoff_factor: float = 2.0

    def delay_for_attempt(self, attempt: int) -> float:
        """Calculate delay for the given attempt number.

        :param attempt: Zero-based attempt index.
        :return: Delay in seconds, capped by ``max_delay``.
        """
        delay = self.base_delay * (self.backoff_factor**attempt)
        return min(delay, self.max_delay)


@dataclass(slots=True, frozen=True)
class RetryPolicy:
    """Collection of retry rules.

    Attributes:
        rules: retry rules to apply.
    """

    rules: t.Tuple[RetryRule, ...] = field(default_factory=tuple)

    def find_rule(self, status: int) -> t.Optional[RetryRule]:
        """Find a retry rule matching the given status code.

        :param status: HTTP status code.
        :return: Matching `RetryRule`, or ``None``.
        """
        for rule in self.rules:
            if status in rule.statuses:
                return rule
        return None


@dataclass(slots=True, frozen=True)
class ReconnectPolicy:
    """Reconnection policy for streaming transports.

    Attributes:
        max_reconnects: maximum reconnection attempts, ``-1`` for unlimited.
        delay: initial delay in seconds before first reconnect.
        max_delay: upper bound for the delay after backoff.
        backoff_factor: multiplier applied to delay on each reconnect.
    """

    max_reconnects: int = 10
    delay: float = 0.5
    max_delay: float = 10.0
    backoff_factor: float = 2.0

    def delay_for_attempt(self, attempt: int) -> float:
        """Calculate delay for the given attempt number.

        :param attempt: Zero-based attempt index.
        :return: Delay in seconds, capped by ``max_delay``.
        """
        d = self.delay * (self.backoff_factor**attempt)
        return min(d, self.max_delay)


DEFAULT_RECONNECT_POLICY: t.Final[ReconnectPolicy] = ReconnectPolicy()

DEFAULT_RETRY_POLICY: t.Final[RetryPolicy] = RetryPolicy(
    rules=(
        RetryRule(
            statuses=frozenset({429}),
            max_retries=5,
            base_delay=0.3,
            max_delay=3.0,
            backoff_factor=2.0,
        ),
        RetryRule(
            statuses=frozenset({500, 502, 503, 504}),
            max_retries=3,
            base_delay=0.5,
            max_delay=5.0,
            backoff_factor=2.0,
        ),
    ),
)
