from __future__ import annotations

import typing as t

import aiohttp

from pytonapi.client import BaseClient
from pytonapi.rest.limiter import RateLimiter
from pytonapi.rest.mixin import ResourcesMixin
from pytonapi.types import (
    DEFAULT_RETRY_POLICY,
    NETWORK_BASE_URLS,
    Network,
    RetryPolicy,
)

__all__ = ["TonapiRestClient"]

T = t.TypeVar("T")


class TonapiRestClient(BaseClient, ResourcesMixin):
    """Async client for the TONAPI."""

    def __init__(
        self,
        api_key: str,
        network: Network,
        *,
        base_url: t.Optional[str] = None,
        timeout: float = 10.0,
        session: t.Optional[aiohttp.ClientSession] = None,
        headers: t.Optional[t.Dict[str, str]] = None,
        cookies: t.Optional[t.Dict[str, str]] = None,
        rps_limit: int = 0,
        rps_period: float = 1.0,
        retry_policy: t.Optional[RetryPolicy] = DEFAULT_RETRY_POLICY,
    ) -> None:
        """Initialize the TONAPI client.

        :param api_key: TONAPI key. Get one at https://tonconsole.com/.
        :param network: Target network (``Network.MAINNET`` or ``Network.TESTNET``).
        :param base_url: Custom base URL (overrides ``network``).
        :param timeout: Request timeout in seconds.
        :param session: Optional external ``aiohttp.ClientSession``.
            When provided, the client will not close it — the caller
            is responsible for managing its lifecycle.
        :param headers: Additional HTTP headers sent with every request.
        :param cookies: Additional cookies sent with every request.
        :param rps_limit: Maximum requests per second (``0`` disables limiting).
        :param rps_period: Rate-limiter window in seconds.
        :param retry_policy: Retry policy, or ``None`` to disable retries.
        """
        super().__init__(
            api_key=api_key,
            base_url=base_url or NETWORK_BASE_URLS[network],
            timeout=timeout,
            session=session,
            headers=headers,
            cookies=cookies,
            retry_policy=retry_policy,
        )
        self._rate_limiter: t.Optional[RateLimiter] = (
            RateLimiter(rps=rps_limit, period=rps_period) if rps_limit > 0 else None
        )
        ResourcesMixin.__init__(self, self)

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: t.Optional[t.Dict[str, t.Any]] = None,
        body: t.Optional[t.Any] = None,
        headers: t.Optional[t.Dict[str, t.Any]] = None,
        response_model: t.Optional[t.Type[T]] = None,
    ) -> t.Any:
        """Execute an HTTP request with retry and rate limiting.

        :param method: HTTP method (``GET``, ``POST``, etc.).
        :param path: API path.
        :param params: Query parameters.
        :param body: JSON request body.
        :param headers: Additional request headers.
        :param response_model: Pydantic model to parse response into.
        :return: Parsed model instance, raw dict, or ``None``.
        """
        if self._rate_limiter:
            await self._rate_limiter.acquire()
        return await super().request(
            method,
            path,
            params=params,
            body=body,
            headers=headers,
            response_model=response_model,
        )
