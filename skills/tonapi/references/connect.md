# Connect

2 methods from `tonapi.connect`:

## get_ton_connect_payload

Get a TonConnect authentication payload.

Returns: `dict[str, Any]`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py connect get_ton_connect_payload
```

```python
result = await tonapi.connect.get_ton_connect_payload()
```

## get_account_info_by_state_init

Get account info by state init.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| body | dict | yes | — | Request body with state init |

Returns: `AccountInfoByStateInit`

```python
result = await tonapi.connect.get_account_info_by_state_init(body={"state_init": "..."})
```
