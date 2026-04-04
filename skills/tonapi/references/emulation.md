# Emulation

5 methods from `tonapi.emulation`:

## decode_message

Decode a BOC message.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| body | dict | yes | — | Request body with `boc` field |

Returns: `DecodedMessage`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py emulation decode_message --body '{"boc":"..."}'
```

```python
result = await tonapi.emulation.decode_message(body={"boc": "..."})
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
result = await tonapi.emulation.emulate_message_to_event(body={"boc": "..."})
```

## emulate_message_to_trace

Emulate a message and return the execution trace.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| body | dict | yes | — | Request body with `boc` field |
| ignore_signature_check | bool \| None | no | None | Ignore signature verification |

Returns: `Trace`

```python
result = await tonapi.emulation.emulate_message_to_trace(body={"boc": "..."})
```

## emulate_message_to_wallet

Emulate a message and return wallet consequences.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| body | dict | yes | — | Request body with `boc` field |
| currency | str \| None | no | None | Currency for balance display |
| accept_language | str \| None | no | None | Language for localized content |

Returns: `MessageConsequences`

```python
result = await tonapi.emulation.emulate_message_to_wallet(body={"boc": "..."})
```

## emulate_message_to_account_event

Emulate a message and return account event.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| account_id | str | yes | — | Account address in any form |
| body | dict | yes | — | Request body with `boc` field |
| ignore_signature_check | bool \| None | no | None | Ignore signature verification |
| accept_language | str \| None | no | None | Language for localized content |

Returns: `AccountEvent`

```python
result = await tonapi.emulation.emulate_message_to_account_event("EQ...", body={"boc": "..."})
```
