# Multisig

2 methods from `tonapi.multisig`:

## get_account

Get multisig wallet information.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| account_id | str | yes | — | Multisig account address |

Returns: `Multisig`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py multisig get_account --account-id EQ...
```

```python
result = await tonapi.multisig.get_account("EQ...")
```

## get_order

Get multisig order information.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| account_id | str | yes | — | Multisig order address |

Returns: `MultisigOrder`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py multisig get_order --account-id EQ...
```

```python
result = await tonapi.multisig.get_order("EQ...")
```
