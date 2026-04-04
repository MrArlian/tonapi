# Utilities

4 methods from `tonapi.utilities`:

## get_openapi_json

Get OpenAPI specification in JSON format.

Returns: `dict[str, Any]`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py utilities get_openapi_json
```

```python
result = await tonapi.utilities.get_openapi_json()
```

## get_openapi_yml

Get OpenAPI specification in YAML format.

Returns: `str`

```python
result = await tonapi.utilities.get_openapi_yml()
```

## status

Get TONAPI service status.

Returns: `ServiceStatus`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py utilities status
```

```python
result = await tonapi.utilities.status()
```

## address_parse

Parse an address into all known formats.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| account_id | str | yes | — | Account address in any form |

Returns: `dict[str, Any]`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py utilities address_parse --account-id EQ...
```

```python
result = await tonapi.utilities.address_parse("EQ...")
```
