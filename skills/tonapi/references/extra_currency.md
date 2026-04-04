# Extra Currency

1 method from `tonapi.extra_currency`:

## get_info

Get extra currency information by ID.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| id | int | yes | — | Extra currency ID |

Returns: `EcPreview`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py extra_currency get_info --id 1
```

```python
result = await tonapi.extra_currency.get_info(1)
```
