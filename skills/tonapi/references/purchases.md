# Purchases

1 method from `tonapi.purchases`:

## get_purchase_history

Get purchase history for an account.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| account_id | str | yes | — | Account address in any form |
| before_lt | int \| None | no | None | Cursor for pagination |
| limit | int | no | 100 | Max results |

Returns: `AccountPurchases`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py purchases get_purchase_history --account-id EQ... --limit 10
```

```python
result = await tonapi.purchases.get_purchase_history("EQ...", limit=10)
```
