# Lite Server

16 methods from `tonapi.lite_server` — raw liteserver protocol operations for low-level blockchain access. All return `dict[str, Any]`.

## get_raw_masterchain_info

Get raw masterchain info.

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py lite_server get_raw_masterchain_info
```

```python
result = await tonapi.lite_server.get_raw_masterchain_info()
```

## get_raw_masterchain_info_ext

Get extended raw masterchain info.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| mode | int | yes | — | Request mode |

```python
result = await tonapi.lite_server.get_raw_masterchain_info_ext(mode=0)
```

## get_raw_time

Get raw liteserver time.

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py lite_server get_raw_time
```

```python
result = await tonapi.lite_server.get_raw_time()
```

## get_raw_blockchain_block

Get raw block data.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| block_id | str | yes | — | Block ID |

```python
result = await tonapi.lite_server.get_raw_blockchain_block("block_id")
```

## get_raw_blockchain_block_state

Get raw block state.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| block_id | str | yes | — | Block ID |

```python
result = await tonapi.lite_server.get_raw_blockchain_block_state("block_id")
```

## get_raw_blockchain_block_header

Get raw block header.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| block_id | str | yes | — | Block ID |
| mode | int | yes | — | Request mode |

```python
result = await tonapi.lite_server.get_raw_blockchain_block_header("block_id", mode=0)
```

## send_raw_message

Send raw message via liteserver.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| body | dict | yes | — | Message body |

```python
result = await tonapi.lite_server.send_raw_message(body={"body": "..."})
```

## get_raw_account_state

Get raw account state.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| account_id | str | yes | — | Account address in any form |
| target_block | str \| None | no | None | Target block ID |

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py lite_server get_raw_account_state --account-id EQ...
```

```python
result = await tonapi.lite_server.get_raw_account_state("EQ...")
```

## get_raw_shard_info

Get raw shard info.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| block_id | str | yes | — | Block ID |
| workchain | int | yes | — | Workchain ID |
| shard | int | yes | — | Shard ID |
| exact | bool | yes | — | Exact match |

```python
result = await tonapi.lite_server.get_raw_shard_info("block_id", workchain=0, shard=0, exact=True)
```

## get_all_raw_shards_info

Get all raw shards info for a block.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| block_id | str | yes | — | Block ID |

```python
result = await tonapi.lite_server.get_all_raw_shards_info("block_id")
```

## get_raw_transactions

Get raw transactions for an account.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| account_id | str | yes | — | Account address |
| count | int | yes | — | Number of transactions |
| lt | int | yes | — | Logical time |
| hash | str | yes | — | Transaction hash |

```python
result = await tonapi.lite_server.get_raw_transactions("EQ...", count=10, lt=12345, hash="...")
```

## get_raw_list_block_transactions

Get raw list of block transactions.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| block_id | str | yes | — | Block ID |
| mode | int | yes | — | Request mode |
| count | int | yes | — | Number of transactions |
| account_id | str \| None | no | None | Account address filter |
| lt | int \| None | no | None | Logical time filter |

```python
result = await tonapi.lite_server.get_raw_list_block_transactions("block_id", mode=0, count=10)
```

## get_raw_block_proof

Get raw block proof.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| known_block | str | yes | — | Known block ID |
| mode | int | yes | — | Request mode |
| target_block | str \| None | no | None | Target block ID |

```python
result = await tonapi.lite_server.get_raw_block_proof(known_block="...", mode=0)
```

## get_raw_config

Get raw config for a block.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| block_id | str | yes | — | Block ID |
| mode | int | yes | — | Request mode |

```python
result = await tonapi.lite_server.get_raw_config("block_id", mode=0)
```

## get_raw_shard_block_proof

Get raw shard block proof.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| block_id | str | yes | — | Block ID |

```python
result = await tonapi.lite_server.get_raw_shard_block_proof("block_id")
```

## get_out_msg_queue_sizes

Get outgoing message queue sizes.

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py lite_server get_out_msg_queue_sizes
```

```python
result = await tonapi.lite_server.get_out_msg_queue_sizes()
```
