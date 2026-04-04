# DNS

4 methods from `tonapi.dns`:

## get_info

Get DNS domain information.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| domain_name | str | yes | — | Domain name (e.g. "wallet.ton") |

Returns: `DomainInfo`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py dns get_info --domain-name wallet.ton
```

```python
result = await tonapi.dns.get_info("wallet.ton")
```

## resolve

Resolve a DNS domain.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| domain_name | str | yes | — | Domain name |
| filter | bool | no | False | Filter results |

Returns: `DnsRecord`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py dns resolve --domain-name wallet.ton
```

```python
result = await tonapi.dns.resolve("wallet.ton")
```

## get_domain_bids

Get bids for a DNS domain.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| domain_name | str | yes | — | Domain name |

Returns: `DomainBids`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py dns get_domain_bids --domain-name wallet.ton
```

```python
result = await tonapi.dns.get_domain_bids("wallet.ton")
```

## get_all_auctions

Get all active DNS auctions.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| tld | str \| None | no | None | Filter by top-level domain |

Returns: `Auctions`

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/run.py dns get_all_auctions
```

```python
result = await tonapi.dns.get_all_auctions()
```
