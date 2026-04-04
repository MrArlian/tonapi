# Claude Code Plugin — TONAPI

AI plugin for [Claude Code](https://claude.ai/code) — query TON blockchain through natural language.

## Requirements

- Python 3.10+ with `pytonapi` package (`pip install pytonapi`)
- API key from [tonconsole.com](https://tonconsole.com/) (optional — without a key, REST is throttled to ~1 request per 4 seconds)

## Installation

In Claude Code:

```
/plugin marketplace add nessshon/claude-plugins
/plugin install tonapi@nessshon-plugins
```

Or install locally:

```bash
git clone https://github.com/nessshon/tonapi.git
claude --plugin-dir ./tonapi
```

## Configuration

Create `.env` in the project root:

```bash
cp .env.example .env
```

| Variable | Description | Default |
|----------|-------------|---------|
| `TONAPI_API_KEY` | API key from [tonconsole.com](https://tonconsole.com/) | — (optional) |
| `TONAPI_NETWORK` | `mainnet`, `testnet`, or `tetra` | `mainnet` |
| `TONAPI_BASE_URL` | Custom base URL (overrides network) | auto |
| `TONAPI_RPS_LIMIT` | Max requests per period | `0` (disabled) |
| `TONAPI_RPS_PERIOD` | Rate limit period in seconds | `1.0` |

## Structure

```
skills/tonapi/
├── SKILL.md              — skill definition and routing table
├── references/
│   ├── quickstart.md          — setup and first request
│   ├── streaming.md           — SSE and WebSocket subscriptions
│   ├── webhooks.md            — webhook client and event dispatcher
│   ├── accounts.md            — account info, balances, events, jettons, NFTs
│   ├── blockchain.md          — blocks, transactions, validators, config
│   ├── connect.md             — TonConnect operations
│   ├── dns.md                 — DNS domains, auctions, bids
│   ├── emulation.md           — message decoding, simulation
│   ├── events.md              — event retrieval
│   ├── extra_currency.md      — extra currency info
│   ├── gasless.md             — gasless transfers
│   ├── jettons.md             — jetton info, holders, transfers
│   ├── lite_server.md         — raw liteserver operations
│   ├── multisig.md            — multisig wallets, orders
│   ├── nft.md                 — NFT collections, items, history
│   ├── purchases.md           — purchase history
│   ├── rates.md               — token prices, charts, markets
│   ├── staking.md             — staking pools, nominators
│   ├── storage.md             — TON storage providers
│   ├── traces.md              — execution traces
│   ├── utilities.md           — API status, address parsing
│   └── wallet.md              — wallet info, seqno, auth
└── scripts/
    └── run.py                 — CLI runner for executing SDK methods
```
