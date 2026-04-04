"""Universal CLI-to-SDK runner for tonapi.

Usage:
    python3 ${CLAUDE_SKILL_DIR}/scripts/run.py <resource> <method> [--param value ...]
    python3 ${CLAUDE_SKILL_DIR}/scripts/run.py streaming <transport> [--param value ...]

Configuration priority: CLI flags > environment variables > defaults.

Environment variables:
    TONAPI_API_KEY      — API key (optional for REST, required for streaming)
    TONAPI_NETWORK      — "mainnet", "testnet", or "tetra" (default: mainnet)
    TONAPI_BASE_URL     — Custom base URL (overrides network)
    TONAPI_RPS_LIMIT    — Rate limit: requests per period (default: 0, disabled)
    TONAPI_RPS_PERIOD   — Rate limit period in seconds (default: 1.0)
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
import typing as t

from pydantic import BaseModel

from pytonapi.rest import TonapiRestClient
from pytonapi.types import Network


def _parse_value(value: str) -> t.Any:
    """Coerce a CLI string value to the appropriate Python type."""
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    if value.lower() == "none":
        return None
    try:
        return int(value)
    except ValueError:
        pass
    try:
        parsed = json.loads(value)
        if isinstance(parsed, (dict, list)):
            return parsed
    except (json.JSONDecodeError, ValueError):
        pass
    if "," in value:
        return [v.strip() for v in value.split(",") if v.strip()]
    return value


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="tonapi SDK runner",
        usage="python run.py <resource> <method> [--param value ...]",
    )
    parser.add_argument("resource", help="Resource group (e.g., accounts, jettons) or 'streaming'")
    parser.add_argument("method", nargs="?", help="Method name (or transport for streaming: sse, ws)")

    parser.add_argument("--api-key", default=None, help="API key (default: TONAPI_API_KEY env)")
    parser.add_argument(
        "--network",
        default=None,
        choices=["mainnet", "testnet", "tetra"],
        help="Network (default: mainnet)",
    )
    parser.add_argument("--base-url", default=None, help="Custom base URL")
    parser.add_argument("--rps-limit", type=int, default=None, help="Rate limit (default: 0)")
    parser.add_argument("--rps-period", type=float, default=None, help="Rate limit period (default: 1.0)")

    return parser


def _resolve_config(args: argparse.Namespace) -> dict[str, t.Any]:
    """Resolve configuration with priority: CLI > env > default."""
    api_key = args.api_key if args.api_key is not None else os.getenv("TONAPI_API_KEY", "")
    network_str = args.network or os.getenv("TONAPI_NETWORK", "mainnet")
    base_url = args.base_url or os.getenv("TONAPI_BASE_URL")
    rps_limit = args.rps_limit if args.rps_limit is not None else int(os.getenv("TONAPI_RPS_LIMIT", "0"))
    rps_period = args.rps_period if args.rps_period is not None else float(os.getenv("TONAPI_RPS_PERIOD", "1.0"))

    network_map = {
        "mainnet": Network.MAINNET,
        "testnet": Network.TESTNET,
        "tetra": Network.TETRA,
    }
    network = network_map.get(network_str.lower(), Network.MAINNET)

    config: dict[str, t.Any] = {
        "api_key": api_key,
        "network": network,
        "rps_limit": rps_limit,
        "rps_period": rps_period,
    }
    if base_url:
        config["base_url"] = base_url

    return config


def _extract_method_kwargs(remaining: list[str]) -> dict[str, t.Any]:
    """Parse remaining CLI args as --param-name value pairs into kwargs."""
    kwargs: dict[str, t.Any] = {}
    i = 0
    while i < len(remaining):
        arg = remaining[i]
        if not arg.startswith("--"):
            i += 1
            continue
        key = arg.lstrip("-").replace("-", "_")
        if i + 1 < len(remaining) and not remaining[i + 1].startswith("--"):
            value = remaining[i + 1]
            kwargs[key] = _parse_value(value)
            i += 2
        else:
            kwargs[key] = True
            i += 1
    return kwargs


def _err(msg: str) -> t.NoReturn:
    """Write error to stderr and exit."""
    sys.stderr.write(msg + "\n")
    sys.exit(1)


def _info(msg: str) -> None:
    """Write info message to stderr."""
    sys.stderr.write(msg + "\n")


def _format_result(result: t.Any) -> str:
    """Format the API result for output."""
    if isinstance(result, BaseModel):
        return result.model_dump_json(indent=2)
    if isinstance(result, list):
        items = []
        for item in result:
            if isinstance(item, BaseModel):
                items.append(item.model_dump(mode="json"))
            else:
                items.append(item)
        return json.dumps(items, indent=2, ensure_ascii=False)
    if isinstance(result, dict):
        return json.dumps(result, indent=2, ensure_ascii=False)
    if isinstance(result, bytes):
        return f"<binary data: {len(result)} bytes>"
    return str(result)


async def _run_rest(
    resource: str,
    method: str,
    kwargs: dict[str, t.Any],
    config: dict[str, t.Any],
) -> None:
    """Execute a REST API method."""
    async with TonapiRestClient(**config) as client:
        resource_obj = getattr(client, resource, None)
        if resource_obj is None:
            available = [a for a in dir(client) if not a.startswith("_") and not callable(getattr(client, a, None))]
            _err(f"Error: unknown resource '{resource}'. Available: {', '.join(available)}")

        method_fn = getattr(resource_obj, method, None)
        if method_fn is None:
            available = [a for a in dir(resource_obj) if not a.startswith("_") and callable(getattr(resource_obj, a))]
            _err(f"Error: unknown method '{method}'. Available: {', '.join(available)}")

        result = await method_fn(**kwargs)
        sys.stdout.write(_format_result(result) + "\n")


async def _run_streaming(
    transport: str,
    kwargs: dict[str, t.Any],
    config: dict[str, t.Any],
) -> None:
    """Execute a streaming subscription for a limited duration."""
    api_key = config.get("api_key", "")
    if not api_key:
        _err("Error: streaming requires an API key.\n      Set TONAPI_API_KEY env var or pass --api-key.")

    from pytonapi.streaming import TonapiStreaming
    from pytonapi.types import Workchain

    duration = kwargs.pop("duration", 60)
    subscribe_types = kwargs.pop("subscribe", "transactions")
    if isinstance(subscribe_types, str):
        subscribe_types = [s.strip() for s in subscribe_types.split(",")]

    accounts_raw = kwargs.pop("accounts", None)
    accounts = accounts_raw if isinstance(accounts_raw, list) else ([accounts_raw] if accounts_raw else None)

    operations_raw = kwargs.pop("operations", None)
    operations = operations_raw if isinstance(operations_raw, list) else [operations_raw] if operations_raw else None

    workchain_raw = kwargs.pop("workchain", None)
    workchain: Workchain | None = None
    if workchain_raw is not None:
        workchain = Workchain(int(workchain_raw))

    streaming = TonapiStreaming(
        api_key,
        config["network"],
        base_url=config.get("base_url"),
    )

    stop_event = asyncio.Event()

    async def _stop_after(seconds: float) -> None:
        await asyncio.sleep(seconds)
        stop_event.set()

    stop_task = asyncio.create_task(_stop_after(float(duration)))

    transport_obj = getattr(streaming, transport, None)
    if transport_obj is None:
        _err(f"Error: unknown transport '{transport}'. Use sse or ws.")

    async def _consume(sub_type: str) -> None:
        subscribe_method = getattr(transport_obj, f"subscribe_{sub_type}", None)
        if subscribe_method is None:
            _info(f"Warning: unknown subscription type '{sub_type}', skipping.")
            _info("Available: transactions, blocks, traces, mempool")
            return

        sub_kwargs: dict[str, t.Any] = {"stop": stop_event}
        if sub_type in ("transactions", "traces", "mempool") and accounts:
            sub_kwargs["accounts"] = accounts
        if sub_type == "transactions" and operations:
            sub_kwargs["operations"] = operations
        if sub_type == "blocks" and workchain is not None:
            sub_kwargs["workchain"] = workchain

        async for event in subscribe_method(**sub_kwargs):
            data = event.model_dump(mode="json") if isinstance(event, BaseModel) else str(event)
            output = json.dumps(
                {"event": sub_type, "data": data},
                indent=2,
                ensure_ascii=False,
            )
            sys.stdout.write(output + "\n")

    async with streaming:
        tasks = [asyncio.create_task(_consume(st)) for st in subscribe_types]
        await asyncio.gather(*tasks, return_exceptions=True)

    stop_task.cancel()


def _load_dotenv() -> None:
    """Load .env file into os.environ if it exists. Does not override existing variables."""
    env_path = os.path.join(os.getcwd(), ".env")
    if not os.path.isfile(env_path):
        return
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip("\"'")
            if key and key not in os.environ:
                os.environ[key] = value


def main() -> None:
    """CLI entry point."""
    _load_dotenv()
    parser = _build_parser()
    args, remaining = parser.parse_known_args()
    config = _resolve_config(args)

    if args.resource == "streaming":
        if not args.method:
            _err("Error: transport required for streaming (sse or ws).")
        kwargs = _extract_method_kwargs(remaining)
        asyncio.run(_run_streaming(args.method, kwargs, config))
        return

    if not args.method:
        _err("Error: method name required for REST calls.")

    if not config.get("api_key"):
        _info(
            "Info: No API key configured. REST works without a key (~0.24 RPS throttle).\n"
            "      For higher limits, get a key at https://tonconsole.com/\n"
            "      Set TONAPI_API_KEY env var or pass --api-key."
        )

    kwargs = _extract_method_kwargs(remaining)
    asyncio.run(_run_rest(args.resource, args.method, kwargs, config))


if __name__ == "__main__":
    main()
