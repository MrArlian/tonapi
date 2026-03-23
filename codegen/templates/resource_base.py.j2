from __future__ import annotations

import typing as t

if t.TYPE_CHECKING:
    from pytonapi.rest.client import TonapiRestClient

__all__ = [
    "BaseResource",
]

_T = t.TypeVar("_T")


class BaseResource:
    """Base class for all API resource groups."""

    def __init__(self, client: TonapiRestClient) -> None:
        self._client = client

    @t.overload
    async def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, t.Any] | None = None,
        body: t.Any | None = None,
        headers: dict[str, t.Any] | None = None,
        response_model: type[_T],
    ) -> _T: ...

    @t.overload
    async def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, t.Any] | None = None,
        body: t.Any | None = None,
        headers: dict[str, t.Any] | None = None,
        response_model: None = None,
    ) -> t.Any: ...

    async def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, t.Any] | None = None,
        body: t.Any | None = None,
        headers: dict[str, t.Any] | None = None,
        response_model: type[_T] | None = None,
    ) -> _T | t.Any:
        """Delegate an HTTP request to the underlying client.

        :param method: HTTP method.
        :param path: API path.
        :param params: query parameters.
        :param body: JSON request body.
        :param headers: additional request headers.
        :param response_model: Pydantic model to parse the response.
        :return: parsed model instance, raw dict, or ``None``.
        """
        return await self._client.request(
            method,
            path,
            params=params,
            body=body,
            headers=headers,
            response_model=response_model,
        )
