# Gasless

3 methods from `tonapi.gasless`:

## config

Get gasless transfer configuration.

Returns: `GaslessConfig`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py gasless config
```

```python
result = await tonapi.gasless.config()
```

## estimate

Estimate gasless transfer parameters.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| master_id | str | yes | — | Jetton master address |
| body | dict | yes | — | Request body with transfer details |
| accept_language | str \| None | no | None | Language for localized content |

Returns: `SignRawParams`

```python
result = await tonapi.gasless.estimate("EQ...", body={...})
```

## send

Send a gasless transfer.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| body | dict | yes | — | Signed transaction body |

Returns: `GaslessTx`

```python
result = await tonapi.gasless.send(body={...})
```
