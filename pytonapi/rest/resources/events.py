# This file is auto-generated. Do not edit manually.

from __future__ import annotations

import typing as t

from pytonapi.rest.models import Event
from pytonapi.rest.resources._base import BaseResource


class EventsResource(BaseResource):
    async def get_event(
        self,
        event_id: str,
        accept_language: t.Optional[str] = None,
    ) -> Event:
        """
        Get an event either by event ID or a hash of any transaction in a trace. An
        event is built on top of a trace which is a series of transactions caused by one
        inbound message. TonAPI looks for known patterns inside the trace and splits the
        trace into actions, where a single action represents a meaningful high-level
        operation like a Jetton Transfer or an NFT Purchase. Actions are expected to be
        shown to users. It is advised not to build any logic on top of actions because
        actions can be changed at any time.

        :param event_id: Event ID or transaction hash in hex (without 0x) or base64url
            format.
        :param accept_language: Accept language.
        :return: Event
        """
        path = f"/v2/events/{event_id}"
        headers = {"Accept-Language": accept_language}
        return await self._request(
            method="GET",
            path=path,
            headers=headers,
            response_model=Event,
        )

    async def emulate_message_to_event(
        self,
        body: t.Dict[str, t.Any],
        ignore_signature_check: t.Optional[bool] = None,
        accept_language: t.Optional[str] = None,
    ) -> Event:
        """
        Emulate sending message to retrieve general blockchain events.

        :param body: Request body.
        :param ignore_signature_check: Ignore signature check.
        :param accept_language: Accept language.
        :return: Event
        """
        path = "/v2/events/emulate"
        params = {"ignore_signature_check": ignore_signature_check}
        headers = {"Accept-Language": accept_language}
        return await self._request(
            method="POST",
            path=path,
            params=params,
            body=body,
            headers=headers,
            response_model=Event,
        )
