# This file is auto-generated. Do not edit manually.

from __future__ import annotations

import typing as t

from pydantic import BaseModel, ConfigDict, Field

from pytonapi.rest.models._enums import (
    AccountStatus,
    AccStatusChange,
    BouncePhaseType,
    ComputeSkipReason,
    TransactionType,
)

if t.TYPE_CHECKING:
    from pytonapi.rest.models.accounts import AccountAddress
    from pytonapi.rest.models.extra_currency import EcPreview


class AccountStorageInfo(BaseModel):
    used_cells: int
    used_bits: int
    used_public_cells: int
    last_paid: int
    due_payment: int


class ActionPhase(BaseModel):
    success: bool
    result_code: int
    total_actions: int
    skipped_actions: int
    fwd_fees: int
    total_fees: int
    result_code_description: t.Optional[str] = Field(default=None)


class BlockCurrencyCollection(BaseModel):
    grams: int
    other: t.List[t.Any]


class BlockParamLimits(BaseModel):
    underload: int
    soft_limit: int
    hard_limit: int


class BlockLimits(BaseModel):
    bytes: BlockParamLimits
    gas: BlockParamLimits
    lt_delta: BlockParamLimits


class BlockValueFlow(BaseModel):
    from_prev_blk: BlockCurrencyCollection
    to_next_blk: BlockCurrencyCollection
    imported: BlockCurrencyCollection
    exported: BlockCurrencyCollection
    fees_collected: BlockCurrencyCollection
    fees_imported: BlockCurrencyCollection
    recovered: BlockCurrencyCollection
    created: BlockCurrencyCollection
    minted: BlockCurrencyCollection
    burned: t.Optional[BlockCurrencyCollection] = Field(default=None)


class Method(BaseModel):
    id: int
    method: str


class SourceFile(BaseModel):
    name: str
    content: str
    is_entrypoint: bool
    is_std_lib: bool
    include_in_command: bool


class Source(BaseModel):
    files: t.List[SourceFile]


class BlockchainAccountInspect(BaseModel):
    code: str
    code_hash: str
    methods: t.List[Method]
    compiler: str
    disassembled_code: t.Optional[str] = Field(default=None)
    source: t.Optional[Source] = Field(default=None)


class BlockchainBlock(BaseModel):
    tx_quantity: int
    value_flow: BlockValueFlow
    workchain_id: int
    shard: str
    seqno: int
    root_hash: str
    file_hash: str
    global_id: int
    version: int
    after_merge: bool
    before_split: bool
    after_split: bool
    want_split: bool
    want_merge: bool
    key_block: bool
    gen_utime: int
    start_lt: int
    end_lt: int
    vert_seqno: int
    gen_catchain_seqno: int
    min_ref_mc_seqno: int
    prev_key_block_seqno: int
    prev_refs: t.List[str]
    in_msg_descr_length: int
    out_msg_descr_length: int
    rand_seed: str
    created_by: str
    gen_software_version: t.Optional[int] = Field(default=None)
    gen_software_capabilities: t.Optional[int] = Field(default=None)
    master_ref: t.Optional[str] = Field(default=None)


class BlockchainBlockShards(BaseModel):
    shards: t.List[t.Any]


class BlockchainBlocks(BaseModel):
    blocks: t.List[BlockchainBlock]


class ValidatorsSet(BaseModel):
    utime_since: int
    utime_until: int
    total: int
    main: int
    list: t.List[t.Any]
    total_weight: t.Optional[str] = Field(default=None)


class BlockchainConfig(BaseModel):
    raw: str
    p0: str = Field(alias="0")
    p1: str = Field(alias="1")
    p2: str = Field(alias="2")
    p4: str = Field(alias="4")
    p44: t.Any = Field(alias="44")
    p3: t.Optional[str] = Field(alias="3", default=None)
    p5: t.Optional[t.Any] = Field(alias="5", default=None)
    p6: t.Optional[t.Any] = Field(alias="6", default=None)
    p7: t.Optional[t.Any] = Field(alias="7", default=None)
    p8: t.Optional[t.Any] = Field(alias="8", default=None)
    p9: t.Optional[t.Any] = Field(alias="9", default=None)
    p10: t.Optional[t.Any] = Field(alias="10", default=None)
    p11: t.Optional[t.Any] = Field(alias="11", default=None)
    p12: t.Optional[t.Any] = Field(alias="12", default=None)
    p13: t.Optional[t.Any] = Field(alias="13", default=None)
    p14: t.Optional[t.Any] = Field(alias="14", default=None)
    p15: t.Optional[t.Any] = Field(alias="15", default=None)
    p16: t.Optional[t.Any] = Field(alias="16", default=None)
    p17: t.Optional[t.Any] = Field(alias="17", default=None)
    p18: t.Optional[t.Any] = Field(alias="18", default=None)
    p20: t.Optional[t.Any] = Field(alias="20", default=None)
    p21: t.Optional[t.Any] = Field(alias="21", default=None)
    p22: t.Optional[t.Any] = Field(alias="22", default=None)
    p23: t.Optional[t.Any] = Field(alias="23", default=None)
    p24: t.Optional[t.Any] = Field(alias="24", default=None)
    p25: t.Optional[t.Any] = Field(alias="25", default=None)
    p28: t.Optional[t.Any] = Field(alias="28", default=None)
    p29: t.Optional[t.Any] = Field(alias="29", default=None)
    p31: t.Optional[t.Any] = Field(alias="31", default=None)
    p32: t.Optional[ValidatorsSet] = Field(alias="32", default=None)
    p33: t.Optional[ValidatorsSet] = Field(alias="33", default=None)
    p34: t.Optional[ValidatorsSet] = Field(alias="34", default=None)
    p35: t.Optional[ValidatorsSet] = Field(alias="35", default=None)
    p36: t.Optional[ValidatorsSet] = Field(alias="36", default=None)
    p37: t.Optional[ValidatorsSet] = Field(alias="37", default=None)
    p40: t.Optional[t.Any] = Field(alias="40", default=None)
    p43: t.Optional[t.Any] = Field(alias="43", default=None)
    p45: t.Optional[t.Any] = Field(alias="45", default=None)
    p71: t.Optional[t.Any] = Field(alias="71", default=None)
    p72: t.Optional[t.Any] = Field(alias="72", default=None)
    p73: t.Optional[t.Any] = Field(alias="73", default=None)
    p79: t.Optional[t.Any] = Field(alias="79", default=None)
    p81: t.Optional[t.Any] = Field(alias="81", default=None)
    p82: t.Optional[t.Any] = Field(alias="82", default=None)

    model_config = ConfigDict(populate_by_name=True)


class BlockchainLibrary(BaseModel):
    boc: str


class ExtraCurrency(BaseModel):
    amount: str
    preview: EcPreview


class BlockchainRawAccount(BaseModel):
    address: str
    balance: int
    last_transaction_lt: int
    status: AccountStatus
    storage: AccountStorageInfo
    extra_balance: t.Optional[t.List[ExtraCurrency]] = Field(default=None)
    code: t.Optional[str] = Field(default=None)
    data: t.Optional[str] = Field(default=None)
    last_transaction_hash: t.Optional[str] = Field(default=None)
    frozen_hash: t.Optional[str] = Field(default=None)
    libraries: t.Optional[t.List[t.Any]] = Field(default=None)


class ComputePhase(BaseModel):
    skipped: bool
    skip_reason: t.Optional[ComputeSkipReason] = Field(default=None)
    success: t.Optional[bool] = Field(default=None)
    gas_fees: t.Optional[int] = Field(default=None)
    gas_used: t.Optional[int] = Field(default=None)
    vm_steps: t.Optional[int] = Field(default=None)
    exit_code: t.Optional[int] = Field(default=None)
    exit_code_description: t.Optional[str] = Field(default=None)


class ConfigProposalSetup(BaseModel):
    min_tot_rounds: int
    max_tot_rounds: int
    min_wins: int
    max_losses: int
    min_store_sec: int
    max_store_sec: int
    bit_price: int
    cell_price: int


class CreditPhase(BaseModel):
    fees_collected: int
    credit: int


class Error(BaseModel):
    error: str


class GasLimitPrices(BaseModel):
    gas_price: int
    gas_limit: int
    gas_credit: int
    block_gas_limit: int
    freeze_due_limit: int
    delete_due_limit: int
    special_gas_limit: t.Optional[int] = Field(default=None)
    flat_gas_limit: t.Optional[int] = Field(default=None)
    flat_gas_price: t.Optional[int] = Field(default=None)


class JettonBridgePrices(BaseModel):
    bridge_burn_fee: int
    bridge_mint_fee: int
    wallet_min_tons_for_storage: int
    wallet_gas_consumption: int
    minter_min_tons_for_storage: int
    discover_gas_consumption: int


class Oracle(BaseModel):
    address: str
    secp_pubkey: str


class JettonBridgeParams(BaseModel):
    bridge_address: str
    oracles_address: str
    state_flags: int
    oracles: t.List[Oracle]
    burn_bridge_fee: t.Optional[int] = Field(default=None)
    external_chain_address: t.Optional[str] = Field(default=None)
    prices: t.Optional[JettonBridgePrices] = Field(default=None)


class StateInit(BaseModel):
    boc: str
    interfaces: t.List[str]


class Message(BaseModel):
    msg_type: str
    created_lt: int
    ihr_disabled: bool
    bounce: bool
    bounced: bool
    value: int
    fwd_fee: int
    ihr_fee: int
    import_fee: int
    created_at: int
    hash: str
    value_extra: t.Optional[t.List[ExtraCurrency]] = Field(default=None)
    destination: t.Optional[AccountAddress] = Field(default=None)
    source: t.Optional[AccountAddress] = Field(default=None)
    op_code: t.Optional[str] = Field(default=None)
    init: t.Optional[StateInit] = Field(default=None)
    raw_body: t.Optional[str] = Field(default=None)
    decoded_op_name: t.Optional[str] = Field(default=None)
    decoded_body: t.Optional[t.Any] = Field(default=None)


class TvmStackRecord(BaseModel):
    type: str
    cell: t.Optional[str] = Field(default=None)
    slice: t.Optional[str] = Field(default=None)
    num: t.Optional[str] = Field(default=None)
    tuple: t.Optional[t.List[TvmStackRecord]] = Field(default=None)


class MethodExecutionResult(BaseModel):
    success: bool
    exit_code: int
    stack: t.List[TvmStackRecord]
    decoded: t.Optional[t.Any] = Field(default=None)


class MisbehaviourPunishmentConfig(BaseModel):
    default_flat_fine: int
    default_proportional_fine: int
    severity_flat_mult: int
    severity_proportional_mult: int
    unpunishable_interval: int
    long_interval: int
    long_flat_mult: int
    long_proportional_mult: int
    medium_interval: int
    medium_flat_mult: int
    medium_proportional_mult: int


class MsgForwardPrices(BaseModel):
    lump_price: int
    bit_price: int
    cell_price: int
    ihr_price_factor: int
    first_frac: int
    next_frac: int


class OracleBridgeParams(BaseModel):
    bridge_addr: str
    oracle_multisig_address: str
    external_chain_address: str
    oracles: t.List[Oracle]


class RawBlockchainConfig(BaseModel):
    config: t.Dict[str, t.Any]


class ReducedBlock(BaseModel):
    workchain_id: int
    shard: str
    seqno: int
    tx_quantity: int
    utime: int
    shards_blocks: t.List[str]
    parent: t.List[str]
    master_ref: t.Optional[str] = Field(default=None)


class ReducedBlocks(BaseModel):
    blocks: t.List[ReducedBlock]


class SizeLimitsConfig(BaseModel):
    max_msg_bits: int
    max_msg_cells: int
    max_library_cells: int
    max_vm_data_depth: int
    max_ext_msg_size: int
    max_ext_msg_depth: int
    max_acc_state_cells: t.Optional[int] = Field(default=None)
    max_acc_state_bits: t.Optional[int] = Field(default=None)


class StoragePhase(BaseModel):
    fees_collected: int
    status_change: AccStatusChange
    fees_due: t.Optional[int] = Field(default=None)


class Transaction(BaseModel):
    hash: str
    lt: int
    account: AccountAddress
    success: bool
    utime: int
    orig_status: AccountStatus
    end_status: AccountStatus
    total_fees: int
    end_balance: int
    transaction_type: TransactionType
    state_update_old: str
    state_update_new: str
    out_msgs: t.List[Message]
    block: str
    aborted: bool
    destroyed: bool
    raw: str
    in_msg: t.Optional[Message] = Field(default=None)
    prev_trans_hash: t.Optional[str] = Field(default=None)
    prev_trans_lt: t.Optional[int] = Field(default=None)
    compute_phase: t.Optional[ComputePhase] = Field(default=None)
    storage_phase: t.Optional[StoragePhase] = Field(default=None)
    credit_phase: t.Optional[CreditPhase] = Field(default=None)
    action_phase: t.Optional[ActionPhase] = Field(default=None)
    bounce_phase: t.Optional[BouncePhaseType] = Field(default=None)


class Transactions(BaseModel):
    transactions: t.List[Transaction]


class Validator(BaseModel):
    address: str
    adnl_address: str
    stake: int
    max_factor: int


class Validators(BaseModel):
    elect_at: int
    elect_close: int
    min_stake: int
    total_stake: int
    validators: t.List[Validator]


class WorkchainDescr(BaseModel):
    workchain: int
    enabled_since: int
    actual_min_split: int
    min_split: int
    max_split: int
    basic: int
    active: bool
    accept_msgs: bool
    flags: int
    zerostate_root_hash: str
    zerostate_file_hash: str
    version: int
