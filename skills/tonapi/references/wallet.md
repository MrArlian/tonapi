# Wallet

6 methods from `tonapi.wallet`:

## ton_connect_proof

Verify TonConnect proof.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| body | dict | yes | — | Proof payload |

Returns: `dict[str, Any]`

```python
result = await tonapi.wallet.ton_connect_proof(body={...})
```

## get_account_seqno

Get wallet sequence number.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| account_id | str | yes | — | Wallet address |

Returns: `Seqno`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py wallet get_account_seqno --account-id EQ...
```

```python
result = await tonapi.wallet.get_account_seqno("EQ...")
```

## get_info

Get wallet information.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| account_id | str | yes | — | Wallet address |

Returns: `Wallet`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py wallet get_info --account-id EQ...
```

```python
result = await tonapi.wallet.get_info("EQ...")
```

## get_wallets_by_public_key

Get wallets associated with a public key.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| public_key | str | yes | — | Public key (hex) |

Returns: `Wallets`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py wallet get_wallets_by_public_key --public-key ...
```

```python
result = await tonapi.wallet.get_wallets_by_public_key("public_key_hex")
```

## get_wallets_by_public_key_bulk

Get wallets for multiple public keys in bulk.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| body | dict | yes | — | Request body with public keys |

Returns: `WalletsByPublicKeys`

```python
result = await tonapi.wallet.get_wallets_by_public_key_bulk(body={"public_keys": ["..."]})
```

## emulate_message_to_wallet

Emulate a message and get wallet consequences.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| body | dict | yes | — | Request body with `boc` field |
| currency | str \| None | no | None | Currency for balance display |
| accept_language | str \| None | no | None | Language for localized content |

Returns: `MessageConsequences`

```python
result = await tonapi.wallet.emulate_message_to_wallet(body={"boc": "..."})
```
