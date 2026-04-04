# Staking

4 methods from `tonapi.staking`:

## get_account_nominators_pools

Get nominator pools for an account.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| account_id | str | yes | — | Account address in any form |

Returns: `AccountStaking`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py staking get_account_nominators_pools --account-id EQ...
```

```python
result = await tonapi.staking.get_account_nominators_pools("EQ...")
```

## get_pool_info

Get staking pool information.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| account_id | str | yes | — | Pool address |
| accept_language | str \| None | no | None | Language for localized content |

Returns: `dict[str, Any]`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py staking get_pool_info --account-id EQ...
```

```python
result = await tonapi.staking.get_pool_info("EQ...")
```

## get_pool_history

Get staking pool history.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| account_id | str | yes | — | Pool address |
| before_lt | int \| None | no | None | Cursor for pagination |
| limit | int | no | 100 | Max results |

Returns: `dict[str, Any]`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py staking get_pool_history --account-id EQ... --limit 10
```

```python
result = await tonapi.staking.get_pool_history("EQ...", limit=10)
```

## get_pools

Get available staking pools.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| available_for | str \| None | no | None | Filter pools available for this address |
| include_unverified | bool \| None | no | None | Include unverified pools |
| accept_language | str \| None | no | None | Language for localized content |

Returns: `dict[str, Any]`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py staking get_pools
```

```python
result = await tonapi.staking.get_pools()
```
