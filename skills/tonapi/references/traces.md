# Traces

2 methods from `tonapi.traces`:

## get_trace

Get execution trace by ID.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| trace_id | str | yes | — | Trace ID |

Returns: `Trace`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py traces get_trace --trace-id ...
```

```python
result = await tonapi.traces.get_trace("trace_id")
```

## emulate_message_to_trace

Emulate a message and return execution trace.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| body | dict | yes | — | Request body with `boc` field |
| ignore_signature_check | bool \| None | no | None | Ignore signature verification |

Returns: `Trace`

```python
result = await tonapi.traces.emulate_message_to_trace(body={"boc": "..."})
```
