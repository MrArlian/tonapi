# This file is auto-generated. Do not edit manually.

from __future__ import annotations

import typing as t

from pytonapi.rest.models import Trace
from pytonapi.rest.resources._base import BaseResource


class TracesResource(BaseResource):
    """TracesResource resource group."""

    async def get_trace(
        self,
        trace_id: str,
    ) -> Trace:
        """Get the trace by trace ID or hash of any transaction in trace.

        :param trace_id: Trace ID or transaction hash in hex (without 0x) or base64url format.
        :return: Trace
        """
        path = f"/v2/traces/{trace_id}"
        return await self._request(
            method="GET",
            path=path,
            response_model=Trace,
        )

    async def emulate_message_to_trace(
        self,
        body: dict[str, t.Any],
        ignore_signature_check: bool | None = None,
    ) -> Trace:
        """Emulate sending message to retrieve with a detailed execution trace.

        :param body: Request body.
        :param ignore_signature_check: Ignore signature check.
        :return: Trace
        """
        path = "/v2/traces/emulate"
        params = {"ignore_signature_check": ignore_signature_check}
        return await self._request(
            method="POST",
            path=path,
            params=params,
            body=body,
            response_model=Trace,
        )
