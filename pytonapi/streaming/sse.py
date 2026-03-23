import asyncio
import json
import typing as t

import aiohttp

from pytonapi.exceptions import (
    STREAMING_RECOVERABLE,
    TONAPIConnectionLostError,
    TONAPIError,
    TONAPIStreamingError,
    raise_for_status,
)
from pytonapi.streaming.models import (
    BlockEvent,
    MempoolEvent,
    TraceEvent,
    TransactionEvent,
)
from pytonapi.types import (
    DEFAULT_RECONNECT_POLICY,
    ReconnectPolicy,
    Workchain,
)


class TonapiSSE:
    """SSE streaming transport for TONAPI."""

    _HEARTBEAT_TIMEOUT: t.Final[float] = 15.0

    def __init__(
        self,
        base_url: str,
        session: aiohttp.ClientSession,
        reconnect_policy: ReconnectPolicy = DEFAULT_RECONNECT_POLICY,
    ) -> None:
        """Initialize SSE transport.

        :param base_url: Base API URL.
        :param session: Shared ``aiohttp.ClientSession``.
        :param reconnect_policy: Reconnection policy.
        """
        self._base_url = base_url.rstrip("/")
        self._session = session
        self._reconnect_policy = reconnect_policy

    async def subscribe_transactions(
        self,
        accounts: list[str] | None = None,
        operations: list[str] | None = None,
        stop: asyncio.Event | None = None,
    ) -> t.AsyncIterator[TransactionEvent]:
        """Subscribe to finalized account transactions.

        :param accounts: Account IDs to track, or ``None`` for all.
        :param operations: Operation filters (opcode names or hex strings).
        :param stop: Event to signal graceful shutdown, or ``None``.
        :return: Async iterator of ``TransactionEvent``.
        """
        params: dict[str, str] = {
            "accounts": ",".join(accounts) if accounts else "ALL",
        }
        if operations:
            params["operations"] = ",".join(operations)

        async for data in self._stream("/v2/sse/accounts/transactions", params, stop):
            yield TransactionEvent.model_validate(data)

    async def subscribe_blocks(
        self,
        workchain: Workchain | None = None,
        stop: asyncio.Event | None = None,
    ) -> t.AsyncIterator[BlockEvent]:
        """Subscribe to new block notifications.

        :param workchain: Workchain filter, or ``None`` for all.
        :param stop: Event to signal graceful shutdown, or ``None``.
        :return: Async iterator of ``BlockEvent``.
        """
        params: dict[str, str] = {}
        if workchain is not None:
            params["workchain"] = str(int(workchain))

        async for data in self._stream("/v2/sse/blocks", params, stop):
            yield BlockEvent.model_validate(data)

    async def subscribe_traces(
        self,
        accounts: list[str] | None = None,
        stop: asyncio.Event | None = None,
    ) -> t.AsyncIterator[TraceEvent]:
        """Subscribe to completed trace notifications.

        :param accounts: Account IDs to track, or ``None`` for all.
        :param stop: Event to signal graceful shutdown, or ``None``.
        :return: Async iterator of ``TraceEvent``.
        """
        params: dict[str, str] = {
            "accounts": ",".join(accounts) if accounts else "ALL",
        }
        async for data in self._stream("/v2/sse/accounts/traces", params, stop):
            yield TraceEvent.model_validate(data)

    async def subscribe_mempool(
        self,
        accounts: list[str] | None = None,
        stop: asyncio.Event | None = None,
    ) -> t.AsyncIterator[MempoolEvent]:
        """Subscribe to pending inbound messages.

        :param accounts: Account IDs to filter, or ``None`` for all.
        :param stop: Event to signal graceful shutdown, or ``None``.
        :return: Async iterator of ``MempoolEvent``.
        """
        params: dict[str, str] = {}
        if accounts:
            params["accounts"] = ",".join(accounts)

        async for data in self._stream("/v2/sse/mempool", params, stop):
            yield MempoolEvent.model_validate(data)

    async def _stream(
        self,
        path: str,
        params: dict[str, str],
        stop: asyncio.Event | None = None,
    ) -> t.AsyncIterator[dict[str, t.Any]]:
        """Open an SSE stream with automatic reconnection.

        :param path: API path.
        :param params: Query parameters.
        :param stop: Event to signal graceful shutdown, or ``None``.
        :return: Async iterator of parsed JSON data dicts.
        :raises TONAPIConnectionLostError: When reconnect limit is exceeded.
        """
        url = f"{self._base_url}{path}"
        attempt = 0

        while not (stop and stop.is_set()):
            try:
                async with self._session.get(url, params=params) as response:
                    if response.status != 200:
                        text = await response.text()
                        content_type = response.headers.get("Content-Type", "")
                        raise_for_status(
                            response.status,
                            text,
                            content_type,
                        )
                    attempt = 0
                    async for data in self._read_events(response, stop):
                        yield data
                    if stop and stop.is_set():
                        return

            except TONAPIError as exc:
                if not isinstance(exc, STREAMING_RECOVERABLE):
                    raise
            except Exception:
                pass

            if stop and stop.is_set():
                return

            attempt += 1
            if (
                self._reconnect_policy.max_reconnects != -1
                and attempt > self._reconnect_policy.max_reconnects
            ):
                raise TONAPIConnectionLostError(attempts=attempt)

            delay = self._reconnect_policy.delay_for_attempt(attempt - 1)
            await asyncio.sleep(delay)

    @classmethod
    async def _read_events(
        cls,
        response: aiohttp.ClientResponse,
        stop: asyncio.Event | None = None,
    ) -> t.AsyncIterator[dict[str, t.Any]]:
        """Parse SSE text/event-stream into JSON data dicts.

        :param response: Aiohttp response with ``text/event-stream`` body.
        :param stop: Event to signal graceful shutdown, or ``None``.
        :return: Async iterator of parsed data dicts.
        :raises TONAPIStreamingError: On heartbeat timeout.
        """
        event_type = ""
        data_buf = ""

        async for raw_line in _read_lines(response, timeout=cls._HEARTBEAT_TIMEOUT):
            if stop and stop.is_set():
                return

            line = raw_line.rstrip("\r\n")

            if not line:
                if event_type == "message" and data_buf:
                    try:
                        parsed = json.loads(data_buf)
                    except json.JSONDecodeError as exc:
                        raise TONAPIStreamingError(
                            f"Invalid SSE JSON: {data_buf}",
                        ) from exc
                    yield parsed
                event_type = ""
                data_buf = ""
                continue

            if line.startswith("event:"):
                event_type = line[6:].strip()
            elif line.startswith("data:"):
                data_buf += line[5:].strip()
            elif line.startswith("id:"):
                pass


async def _read_lines(
    response: aiohttp.ClientResponse,
    *,
    timeout: float,
) -> t.AsyncIterator[str]:
    """Read lines from a streaming response with heartbeat timeout.

    :param response: Aiohttp streaming response.
    :param timeout: Seconds to wait before considering the connection dead.
    :return: Async iterator of raw lines.
    :raises TONAPIStreamingError: On heartbeat timeout.
    """
    buffer = ""
    while True:
        try:
            chunk = await asyncio.wait_for(
                response.content.read(4096),
                timeout=timeout,
            )
        except asyncio.TimeoutError as err:
            raise TONAPIStreamingError("SSE heartbeat timeout") from err

        if not chunk:
            break

        buffer += chunk.decode("utf-8")
        while "\n" in buffer:
            line, buffer = buffer.split("\n", 1)
            yield line
