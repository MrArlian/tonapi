from __future__ import annotations

import typing as t

if t.TYPE_CHECKING:
    from pytonapi.rest.client import TonapiRestClient

__all__ = [
    "BaseResource",
]


class BaseResource:
    """Base class for all API resource groups."""

    def __init__(self, client: TonapiRestClient) -> None:
        self._client = client

    async def _request(
        self,
        method: str,
        path: str,
        *,
        params: t.Optional[t.Dict[str, t.Any]] = None,
        body: t.Optional[t.Any] = None,
        headers: t.Optional[t.Dict[str, t.Any]] = None,
        response_model: t.Optional[t.Type[t.Any]] = None,
    ) -> t.Any:
        """Delegate an HTTP request to the underlying client.

        :param method: HTTP method.
        :param path: API path.
        :param params: Query parameters.
        :param body: JSON request body.
        :param headers: Additional request headers.
        :param response_model: Pydantic model to parse the response.
        :return: Parsed model instance, raw dict, or ``None``.
        """
        return await self._client.request(
            method,
            path,
            params=params,
            body=body,
            headers=headers,
            response_model=response_model,
        )
