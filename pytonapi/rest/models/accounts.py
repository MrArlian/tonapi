# This file is auto-generated. Do not edit manually.

from __future__ import annotations

import typing as t

from pydantic import BaseModel, ConfigDict, Field

from pytonapi.rest.models._enums import (
    AccountStatus,
    ExecGetMethodArgType,
    JettonVerificationType,
    PoolImplementationType,
)

if t.TYPE_CHECKING:
    from pytonapi.rest.models.blockchain import ExtraCurrency
    from pytonapi.rest.models.extra_currency import EcPreview
    from pytonapi.rest.models.jettons import ScaledUI
    from pytonapi.rest.models.multisig import Multisig
    from pytonapi.rest.models.nft import NftItem
    from pytonapi.rest.models.purchases import Metadata, Price
    from pytonapi.rest.models.rates import TokenRates


class Account(BaseModel):
    address: str
    balance: int
    last_activity: int
    status: AccountStatus
    get_methods: t.List[str]
    is_wallet: bool
    extra_balance: t.Optional[t.List[ExtraCurrency]] = Field(default=None)
    currencies_balance: t.Optional[t.Dict[str, t.Any]] = Field(default=None)
    interfaces: t.Optional[t.List[str]] = Field(default=None)
    name: t.Optional[str] = Field(default=None)
    is_scam: t.Optional[bool] = Field(default=None)
    icon: t.Optional[str] = Field(default=None)
    memo_required: t.Optional[bool] = Field(default=None)
    is_suspended: t.Optional[bool] = Field(default=None)


class AccountAddress(BaseModel):
    address: str
    is_scam: bool
    is_wallet: bool
    name: t.Optional[str] = Field(default=None)
    icon: t.Optional[str] = Field(default=None)


class GasRelayAction(BaseModel):
    amount: int
    relayer: AccountAddress
    target: AccountAddress


class EncryptedComment(BaseModel):
    encryption_type: str
    cipher_text: str


class ExtraCurrencyTransferAction(BaseModel):
    sender: AccountAddress
    recipient: AccountAddress
    amount: str
    currency: EcPreview
    comment: t.Optional[str] = Field(default=None)
    encrypted_comment: t.Optional[EncryptedComment] = Field(default=None)


class SetSignatureAllowedAction(BaseModel):
    wallet: AccountAddress
    allowed: bool


class UnSubscriptionAction(BaseModel):
    subscriber: AccountAddress
    subscription: str
    beneficiary: AccountAddress
    admin: AccountAddress


class WithdrawStakeRequestAction(BaseModel):
    staker: AccountAddress
    pool: AccountAddress
    implementation: PoolImplementationType
    amount: t.Optional[int] = Field(default=None)


class JettonPreview(BaseModel):
    address: str
    name: str
    symbol: str
    decimals: int
    image: str
    verification: JettonVerificationType
    score: int
    custom_payload_api_uri: t.Optional[str] = Field(default=None)
    scaled_ui: t.Optional[ScaledUI] = Field(default=None)


class JettonBurnAction(BaseModel):
    sender: AccountAddress
    senders_wallet: str
    amount: str
    jetton: JettonPreview


class ContractDeployAction(BaseModel):
    address: str
    interfaces: t.List[str]


class DomainRenewAction(BaseModel):
    domain: str
    contract_address: str
    renewer: AccountAddress


class ActionSimplePreview(BaseModel):
    name: str
    description: str
    accounts: t.List[AccountAddress]
    action_image: t.Optional[str] = Field(default=None)
    value: t.Optional[str] = Field(default=None)
    value_image: t.Optional[str] = Field(default=None)


class NftPurchaseAction(BaseModel):
    auction_type: str
    amount: Price
    nft: NftItem
    seller: AccountAddress
    buyer: AccountAddress


class ElectionsRecoverStakeAction(BaseModel):
    amount: int
    staker: AccountAddress


class Refund(BaseModel):
    type: str
    origin: str


class SmartContractAction(BaseModel):
    executor: AccountAddress
    contract: AccountAddress
    ton_attached: int
    operation: str
    payload: t.Optional[str] = Field(default=None)
    refund: t.Optional[Refund] = Field(default=None)


class SubscriptionAction(BaseModel):
    subscriber: AccountAddress
    subscription: str
    beneficiary: AccountAddress
    admin: AccountAddress
    price: Price
    initial: bool
    amount: t.Optional[int] = Field(default=None)


class WithdrawStakeAction(BaseModel):
    amount: int
    staker: AccountAddress
    pool: AccountAddress
    implementation: PoolImplementationType


class NftItemTransferAction(BaseModel):
    nft: str
    sender: t.Optional[AccountAddress] = Field(default=None)
    recipient: t.Optional[AccountAddress] = Field(default=None)
    comment: t.Optional[str] = Field(default=None)
    encrypted_comment: t.Optional[EncryptedComment] = Field(default=None)
    payload: t.Optional[str] = Field(default=None)
    refund: t.Optional[Refund] = Field(default=None)


class DepositStakeAction(BaseModel):
    amount: int
    staker: AccountAddress
    pool: AccountAddress
    implementation: PoolImplementationType


class PurchaseAction(BaseModel):
    source: AccountAddress
    destination: AccountAddress
    invoice_id: str
    amount: Price
    metadata: Metadata


class JettonTransferAction(BaseModel):
    senders_wallet: str
    recipients_wallet: str
    amount: str
    jetton: JettonPreview
    sender: t.Optional[AccountAddress] = Field(default=None)
    recipient: t.Optional[AccountAddress] = Field(default=None)
    comment: t.Optional[str] = Field(default=None)
    encrypted_comment: t.Optional[EncryptedComment] = Field(default=None)
    refund: t.Optional[Refund] = Field(default=None)


class FlawedJettonTransferAction(BaseModel):
    senders_wallet: str
    recipients_wallet: str
    sent_amount: str
    received_amount: str
    jetton: JettonPreview
    sender: t.Optional[AccountAddress] = Field(default=None)
    recipient: t.Optional[AccountAddress] = Field(default=None)
    comment: t.Optional[str] = Field(default=None)
    encrypted_comment: t.Optional[EncryptedComment] = Field(default=None)
    refund: t.Optional[Refund] = Field(default=None)


class AddExtensionAction(BaseModel):
    wallet: AccountAddress
    extension: str


class JettonMintAction(BaseModel):
    recipient: AccountAddress
    recipients_wallet: str
    amount: str
    jetton: JettonPreview


class RemoveExtensionAction(BaseModel):
    wallet: AccountAddress
    extension: str


class JettonSwapAction(BaseModel):
    dex: str
    amount_in: str
    amount_out: str
    user_wallet: AccountAddress
    router: AccountAddress
    ton_in: t.Optional[int] = Field(default=None)
    ton_out: t.Optional[int] = Field(default=None)
    jetton_master_in: t.Optional[JettonPreview] = Field(default=None)
    jetton_master_out: t.Optional[JettonPreview] = Field(default=None)


class Protocol(BaseModel):
    name: str
    image: t.Optional[str] = Field(default=None)


class DepositTokenStakeAction(BaseModel):
    staker: AccountAddress
    protocol: Protocol
    stake_meta: t.Optional[Price] = Field(default=None)


class VaultDepositInfo(BaseModel):
    price: Price
    vault: str


class LiquidityDepositAction(BaseModel):
    protocol: Protocol
    from_: AccountAddress = Field(alias="from")
    tokens: t.List[VaultDepositInfo]

    model_config = ConfigDict(populate_by_name=True)


class ElectionsDepositStakeAction(BaseModel):
    amount: int
    staker: AccountAddress


class WithdrawTokenStakeRequestAction(BaseModel):
    staker: AccountAddress
    protocol: Protocol
    stake_meta: t.Optional[Price] = Field(default=None)


class AuctionBidAction(BaseModel):
    auction_type: str
    amount: Price
    bidder: AccountAddress
    auction: AccountAddress
    nft: t.Optional[NftItem] = Field(default=None)


class TonTransferAction(BaseModel):
    sender: AccountAddress
    recipient: AccountAddress
    amount: int
    comment: t.Optional[str] = Field(default=None)
    encrypted_comment: t.Optional[EncryptedComment] = Field(default=None)
    refund: t.Optional[Refund] = Field(default=None)


class Action(BaseModel):
    type: str
    status: str
    simple_preview: ActionSimplePreview
    base_transactions: t.List[str]
    ton_transfer: t.Optional[TonTransferAction] = Field(
        alias="TonTransfer", default=None
    )
    extra_currency_transfer: t.Optional[ExtraCurrencyTransferAction] = Field(
        alias="ExtraCurrencyTransfer", default=None
    )
    contract_deploy: t.Optional[ContractDeployAction] = Field(
        alias="ContractDeploy", default=None
    )
    jetton_transfer: t.Optional[JettonTransferAction] = Field(
        alias="JettonTransfer", default=None
    )
    flawed_jetton_transfer: t.Optional[FlawedJettonTransferAction] = Field(
        alias="FlawedJettonTransfer", default=None
    )
    jetton_burn: t.Optional[JettonBurnAction] = Field(alias="JettonBurn", default=None)
    jetton_mint: t.Optional[JettonMintAction] = Field(alias="JettonMint", default=None)
    nft_item_transfer: t.Optional[NftItemTransferAction] = Field(
        alias="NftItemTransfer", default=None
    )
    subscribe: t.Optional[SubscriptionAction] = Field(alias="Subscribe", default=None)
    un_subscribe: t.Optional[UnSubscriptionAction] = Field(
        alias="UnSubscribe", default=None
    )
    auction_bid: t.Optional[AuctionBidAction] = Field(alias="AuctionBid", default=None)
    nft_purchase: t.Optional[NftPurchaseAction] = Field(
        alias="NftPurchase", default=None
    )
    deposit_stake: t.Optional[DepositStakeAction] = Field(
        alias="DepositStake", default=None
    )
    withdraw_stake: t.Optional[WithdrawStakeAction] = Field(
        alias="WithdrawStake", default=None
    )
    withdraw_stake_request: t.Optional[WithdrawStakeRequestAction] = Field(
        alias="WithdrawStakeRequest", default=None
    )
    elections_deposit_stake: t.Optional[ElectionsDepositStakeAction] = Field(
        alias="ElectionsDepositStake", default=None
    )
    elections_recover_stake: t.Optional[ElectionsRecoverStakeAction] = Field(
        alias="ElectionsRecoverStake", default=None
    )
    jetton_swap: t.Optional[JettonSwapAction] = Field(alias="JettonSwap", default=None)
    smart_contract_exec: t.Optional[SmartContractAction] = Field(
        alias="SmartContractExec", default=None
    )
    domain_renew: t.Optional[DomainRenewAction] = Field(
        alias="DomainRenew", default=None
    )
    purchase: t.Optional[PurchaseAction] = Field(alias="Purchase", default=None)
    add_extension: t.Optional[AddExtensionAction] = Field(
        alias="AddExtension", default=None
    )
    remove_extension: t.Optional[RemoveExtensionAction] = Field(
        alias="RemoveExtension", default=None
    )
    set_signature_allowed_action: t.Optional[SetSignatureAllowedAction] = Field(
        alias="SetSignatureAllowedAction", default=None
    )
    gas_relay: t.Optional[GasRelayAction] = Field(alias="GasRelay", default=None)
    deposit_token_stake: t.Optional[DepositTokenStakeAction] = Field(
        alias="DepositTokenStake", default=None
    )
    withdraw_token_stake_request: t.Optional[WithdrawTokenStakeRequestAction] = Field(
        alias="WithdrawTokenStakeRequest", default=None
    )
    liquidity_deposit: t.Optional[LiquidityDepositAction] = Field(
        alias="LiquidityDeposit", default=None
    )

    model_config = ConfigDict(populate_by_name=True)


class AccountEvent(BaseModel):
    event_id: str
    account: AccountAddress
    timestamp: int
    actions: t.List[Action]
    is_scam: bool
    lt: int
    in_progress: bool
    extra: int
    progress: float
    ext_msg_hash: t.Optional[str] = Field(default=None)


class AccountEvents(BaseModel):
    events: t.List[AccountEvent]
    next_from: int


class Accounts(BaseModel):
    accounts: t.List[Account]


class DnsExpiring(BaseModel):
    items: t.List[t.Any]


class DomainNames(BaseModel):
    domains: t.List[str]


class ExecGetMethodArg(BaseModel):
    type: ExecGetMethodArgType
    value: str


class ExtraCurrencies(BaseModel):
    extra_currencies: t.List[EcPreview]


class FoundAccounts(BaseModel):
    addresses: t.List[t.Any]


class JettonBalance(BaseModel):
    balance: str
    wallet_address: AccountAddress
    jetton: JettonPreview
    price: t.Optional[TokenRates] = Field(default=None)
    extensions: t.Optional[t.List[str]] = Field(default=None)
    lock: t.Optional[t.Any] = Field(default=None)


class JettonOperation(BaseModel):
    operation: str
    utime: int
    lt: int
    transaction_hash: str
    amount: str
    jetton: JettonPreview
    trace_id: str
    query_id: str
    source: t.Optional[AccountAddress] = Field(default=None)
    destination: t.Optional[AccountAddress] = Field(default=None)
    payload: t.Optional[t.Any] = Field(default=None)


class JettonOperations(BaseModel):
    operations: t.List[JettonOperation]
    next_from: t.Optional[int] = Field(default=None)


class JettonsBalances(BaseModel):
    balances: t.List[JettonBalance]


class Multisigs(BaseModel):
    multisigs: t.List[Multisig]


class Subscription(BaseModel):
    type: str
    status: str
    period: int
    subscription_id: str
    payment_per_period: Price
    wallet: AccountAddress
    next_charge_at: int
    metadata: Metadata
    address: t.Optional[str] = Field(default=None)
    beneficiary: t.Optional[AccountAddress] = Field(default=None)
    admin: t.Optional[AccountAddress] = Field(default=None)


class Subscriptions(BaseModel):
    subscriptions: t.List[Subscription]


class TraceID(BaseModel):
    id: str
    utime: int


class TraceIDs(BaseModel):
    traces: t.List[TraceID]
