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


class TonapiWebSocket:
    """WebSocket streaming transport for TONAPI."""

    _METHOD_MAP: t.Final[t.Dict[str, str]] = {
        "subscribe_block": "block",
        "subscribe_account": "account_transaction",
        "subscribe_trace": "trace",
        "subscribe_mempool": "mempool_message",
    }

    def __init__(
        self,
        base_url: str,
        session: aiohttp.ClientSession,
        reconnect_policy: ReconnectPolicy = DEFAULT_RECONNECT_POLICY,
    ) -> None:
        """Initialize WebSocket transport.

        :param base_url: Base API URL (``https://`` is replaced with ``wss://``).
        :param session: Shared ``aiohttp.ClientSession``.
        :param reconnect_policy: Reconnection policy.
        """
        ws_url = base_url.rstrip("/").replace("https://", "wss://")
        self._ws_url = f"{ws_url}/v2/websocket"
        self._session = session
        self._reconnect_policy = reconnect_policy

    async def subscribe_transactions(
        self,
        accounts: t.Optional[t.List[str]] = None,
        operations: t.Optional[t.List[str]] = None,
        stop: t.Optional[asyncio.Event] = None,
    ) -> t.AsyncIterator[TransactionEvent]:
        """Subscribe to finalized account transactions.

        :param accounts: Account IDs to track, or ``None`` for all.
        :param operations: Operation filters (opcode names or hex strings).
        :param stop: Event to signal graceful shutdown, or ``None``.
        :return: Async iterator of ``TransactionEvent``.
        """
        params: t.List[str] = []
        if accounts:
            for acc in accounts:
                if operations:
                    params.append(f"{acc};operations={','.join(operations)}")
                else:
                    params.append(acc)
        else:
            params.append("ALL")

        async for data in self._stream("subscribe_account", params, stop):
            yield TransactionEvent.model_validate(data)

    async def subscribe_blocks(
        self,
        workchain: t.Optional[Workchain] = None,
        stop: t.Optional[asyncio.Event] = None,
    ) -> t.AsyncIterator[BlockEvent]:
        """Subscribe to new block notifications.

        :param workchain: Workchain filter, or ``None`` for all.
        :param stop: Event to signal graceful shutdown, or ``None``.
        :return: Async iterator of ``BlockEvent``.
        """
        params: t.List[str] = []
        if workchain is not None:
            params.append(f"workchain={int(workchain)}")

        async for data in self._stream("subscribe_block", params, stop):
            yield BlockEvent.model_validate(data)

    async def subscribe_traces(
        self,
        accounts: t.Optional[t.List[str]] = None,
        stop: t.Optional[asyncio.Event] = None,
    ) -> t.AsyncIterator[TraceEvent]:
        """Subscribe to completed trace notifications.

        :param accounts: Account IDs to track, or ``None`` for all.
        :param stop: Event to signal graceful shutdown, or ``None``.
        :return: Async iterator of ``TraceEvent``.
        """
        params: t.List[str] = []
        if accounts:
            params.extend(accounts)
        else:
            params.append("ALL")

        async for data in self._stream("subscribe_trace", params, stop):
            yield TraceEvent.model_validate(data)

    async def subscribe_mempool(
        self,
        accounts: t.Optional[t.List[str]] = None,
        stop: t.Optional[asyncio.Event] = None,
    ) -> t.AsyncIterator[MempoolEvent]:
        """Subscribe to pending inbound messages.

        :param accounts: Account IDs to filter, or ``None`` for all.
        :param stop: Event to signal graceful shutdown, or ``None``.
        :return: Async iterator of ``MempoolEvent``.
        """
        params: t.List[str] = []
        if accounts:
            params.append(f"accounts={','.join(accounts)}")

        async for data in self._stream("subscribe_mempool", params, stop):
            yield MempoolEvent.model_validate(data)

    async def _stream(
        self,
        method: str,
        params: t.List[str],
        stop: t.Optional[asyncio.Event] = None,
    ) -> t.AsyncIterator[t.Dict[str, t.Any]]:
        """Open a WebSocket connection with automatic reconnection.

        :param method: JSON-RPC subscribe method name.
        :param params: JSON-RPC params array.
        :param stop: Event to signal graceful shutdown, or ``None``.
        :return: Async iterator of parsed event data dicts.
        :raises TONAPIConnectionLostError: When reconnect limit is exceeded.
        """
        event_method = self._METHOD_MAP[method]
        attempt = 0

        while not (stop and stop.is_set()):
            try:
                async with self._session.ws_connect(self._ws_url) as ws:
                    await self._subscribe(ws, method, params)
                    attempt = 0

                    while True:
                        if stop and stop.is_set():
                            return
                        try:
                            msg = await asyncio.wait_for(
                                ws.receive(),
                                timeout=1.0,
                            )
                        except (asyncio.TimeoutError,):
                            continue
                        if msg.type == aiohttp.WSMsgType.TEXT:
                            data = json.loads(msg.data)
                            if data.get("method") == event_method:
                                yield data["params"]
                        elif msg.type in (
                            aiohttp.WSMsgType.CLOSED,
                            aiohttp.WSMsgType.ERROR,
                            aiohttp.WSMsgType.CLOSING,
                        ):
                            break

            except (aiohttp.WSServerHandshakeError,) as exc:
                raise_for_status(
                    exc.status,
                    exc.message or "",
                    "",
                )
            except (TONAPIError,) as exc:
                if not isinstance(exc, STREAMING_RECOVERABLE):
                    raise
            except (Exception,):
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

    @staticmethod
    async def _subscribe(
        ws: aiohttp.ClientWebSocketResponse,
        method: str,
        params: t.List[str],
    ) -> None:
        """Send a JSON-RPC subscribe request and validate the response.

        :param ws: Active WebSocket connection.
        :param method: JSON-RPC method name.
        :param params: JSON-RPC params array.
        :raises TONAPIStreamingError: On subscription failure.
        """
        request: t.Dict[str, t.Any] = {
            "id": 1,
            "jsonrpc": "2.0",
            "method": method,
        }
        if params:
            request["params"] = params

        await ws.send_json(request)

        response = await ws.receive_json()
        if "error" in response:
            raise TONAPIStreamingError(
                f"WebSocket subscribe failed: {response['error']}",
            )
