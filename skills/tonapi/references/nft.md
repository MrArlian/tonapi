# NFT

8 methods from `tonapi.nft`:

## get_account_nft_history

Get NFT history for an account.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| account_id | str | yes | — | Account address in any form |
| limit | int | yes | — | Max results |
| before_lt | int \| None | no | None | Cursor for pagination |
| accept_language | str \| None | no | None | Language for localized content |

Returns: `NftOperations`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py nft get_account_nft_history --account-id EQ... --limit 10
```

```python
result = await tonapi.nft.get_account_nft_history("EQ...", limit=10)
```

## get_collections

Get NFT collections.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| limit | int | no | 100 | Max results |
| offset | int | no | 0 | Pagination offset |

Returns: `NftCollections`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py nft get_collections --limit 10
```

```python
result = await tonapi.nft.get_collections(limit=10)
```

## get_collection

Get NFT collection by address.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| account_id | str | yes | — | Collection address |

Returns: `NftCollection`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py nft get_collection --account-id EQ...
```

```python
result = await tonapi.nft.get_collection("EQ...")
```

## get_collection_items_by_addresses

Get multiple NFT collections in bulk.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| body | dict | yes | — | Request body with `account_ids` list |

Returns: `NftCollections`

```python
result = await tonapi.nft.get_collection_items_by_addresses(body={"account_ids": ["EQ..."]})
```

## get_items_from_collection

Get items from a specific NFT collection.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| account_id | str | yes | — | Collection address |
| limit | int | no | 1000 | Max results |
| offset | int | no | 0 | Pagination offset |

Returns: `NftItems`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py nft get_items_from_collection --account-id EQ... --limit 10
```

```python
result = await tonapi.nft.get_items_from_collection("EQ...", limit=10)
```

## get_items_by_addresses

Get multiple NFT items in bulk.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| body | dict | yes | — | Request body with `account_ids` list |

Returns: `NftItems`

```python
result = await tonapi.nft.get_items_by_addresses(body={"account_ids": ["EQ..."]})
```

## get_item_by_address

Get a single NFT item.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| account_id | str | yes | — | NFT item address |

Returns: `NftItem`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py nft get_item_by_address --account-id EQ...
```

```python
result = await tonapi.nft.get_item_by_address("EQ...")
```

## get_history_by_id

Get NFT item history.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| account_id | str | yes | — | NFT item address |
| limit | int | yes | — | Max results |
| before_lt | int \| None | no | None | Cursor for pagination |
| start_date | int \| None | no | None | Start date (Unix timestamp) |
| end_date | int \| None | no | None | End date (Unix timestamp) |
| accept_language | str \| None | no | None | Language for localized content |

Returns: `AccountEvents`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py nft get_history_by_id --account-id EQ... --limit 10
```

```python
result = await tonapi.nft.get_history_by_id("EQ...", limit=10)
```
