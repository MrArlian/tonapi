# Events

2 methods from `tonapi.events`:

## get_event

Get event by ID.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| event_id | str | yes | — | Event ID |
| accept_language | str \| None | no | None | Language for localized content |

Returns: `Event`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py events get_event --event-id ...
```

```python
result = await tonapi.events.get_event("event_id")
```

## emulate_message_to_event

Emulate a message and return the resulting event.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| body | dict | yes | — | Request body with `boc` field |
| ignore_signature_check | bool \| None | no | None | Ignore signature verification |
| accept_language | str \| None | no | None | Language for localized content |

Returns: `Event`

```python
result = await tonapi.events.emulate_message_to_event(body={"boc": "..."})
```
