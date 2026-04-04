# Rates

3 methods from `tonapi.rates`:

## get_rates

Get token prices in chosen currencies. For display only — don't use for financial transactions.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| tokens | list[str] | yes | — | Token addresses (accept "ton" and jetton master addresses) |
| currencies | list[str] | yes | — | Currency codes (accept "ton" and fiat currencies like "usd", "eur") |

Returns: `dict[str, Any]`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py rates get_rates --tokens ton --currencies usd
```

```python
result = await tonapi.rates.get_rates(tokens=["ton"], currencies=["usd"])
```

## get_chart_rates

Get price chart for a token.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| token | str | yes | — | Jetton master address or "ton" |
| currency | str \| None | no | None | Currency code |
| start_date | int \| None | no | None | Start date (Unix timestamp) |
| end_date | int \| None | no | None | End date (Unix timestamp) |
| points_count | int | no | 200 | Number of data points |

Returns: `dict[str, Any]`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py rates get_chart_rates --token ton --currency usd --points-count 100
```

```python
result = await tonapi.rates.get_chart_rates(token="ton", currency="usd", points_count=100)
```

## get_markets_rates

Get TON price from markets.

Returns: `dict[str, Any]`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py rates get_markets_rates
```

```python
result = await tonapi.rates.get_markets_rates()
```
