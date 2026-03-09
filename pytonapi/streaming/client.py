from __future__ import annotations

import typing as t

from pytonapi.client import BaseClient
from pytonapi.streaming.sse import TonapiSSE
from pytonapi.streaming.ws import TonapiWebSocket
from pytonapi.types import (
    DEFAULT_RECONNECT_POLICY,
    NETWORK_BASE_URLS,
    Network,
    ReconnectPolicy,
)


class TonapiStreaming(BaseClient):
    """Streaming client for TONAPI SSE and WebSocket APIs."""

    def __init__(
        self,
        api_key: str,
        network: Network,
        *,
        base_url: t.Optional[str] = None,
        headers: t.Optional[t.Dict[str, str]] = None,
        reconnect_policy: t.Optional[ReconnectPolicy] = None,
    ) -> None:
        """Initialize the streaming client.

        :param api_key: TONAPI key. Get one at https://tonconsole.com/.
        :param network: Target network (``Network.MAINNET`` or ``Network.TESTNET``).
        :param base_url: Custom base URL (overrides ``network``).
        :param headers: Additional HTTP headers sent with every request.
        :param reconnect_policy: Reconnection policy, or ``None`` for default.
        """
        resolved_url = base_url or NETWORK_BASE_URLS[network]
        super().__init__(
            api_key=api_key,
            base_url=resolved_url,
            headers=headers,
            timeout=0.0,
        )
        self._reconnect_policy = reconnect_policy or DEFAULT_RECONNECT_POLICY
        self._sse: t.Optional[TonapiSSE] = None
        self._ws: t.Optional[TonapiWebSocket] = None

    @property
    def sse(self) -> TonapiSSE:
        """SSE streaming transport.

        :return: ``TonapiSSE`` instance.
        """
        if self._sse is None:
            self._sse = TonapiSSE(
                base_url=self._base_url,
                session=self._session,
                reconnect_policy=self._reconnect_policy,
            )
        return self._sse

    @property
    def ws(self) -> TonapiWebSocket:
        """WebSocket streaming transport.

        :return: ``TonapiWebSocket`` instance.
        """
        if self._ws is None:
            self._ws = TonapiWebSocket(
                base_url=self._base_url,
                session=self._session,
                reconnect_policy=self._reconnect_policy,
            )
        return self._ws

    async def __aenter__(self) -> TonapiStreaming:
        """Enter the async context manager."""
        await self.create_session()
        return self

    async def __aexit__(
        self,
        exc_type: t.Optional[t.Type[BaseException]],
        exc_val: t.Optional[BaseException],
        exc_tb: t.Optional[t.Any],
    ) -> None:
        """Exit the async context manager."""
        self._sse = None
        self._ws = None
        await self.close_session()
