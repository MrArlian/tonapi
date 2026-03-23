# This file is auto-generated. Do not edit manually.

from __future__ import annotations

import typing as t

from pytonapi.rest.models import AccountEvent, DecodedMessage, Event, MessageConsequences, Trace
from pytonapi.rest.resources._base import BaseResource


class EmulationResource(BaseResource):
    """EmulationResource resource group."""

    async def decode_message(
        self,
        body: dict[str, t.Any],
    ) -> DecodedMessage:
        """Decode a given message. Only external incoming messages can be decoded currently.

        :param body: Request body.
        :return: DecodedMessage
        """
        path = "/v2/message/decode"
        return await self._request(
            method="POST",
            path=path,
            body=body,
            response_model=DecodedMessage,
        )

    async def emulate_message_to_event(
        self,
        body: dict[str, t.Any],
        ignore_signature_check: bool | None = None,
        accept_language: str | None = None,
    ) -> Event:
        """Emulate sending message to retrieve general blockchain events.

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

    async def emulate_message_to_wallet(
        self,
        body: dict[str, t.Any],
        currency: str | None = None,
        accept_language: str | None = None,
    ) -> MessageConsequences:
        """Emulate a wallet message on the current blockchain state and derives its consequences for the signing wallet.

        :param body: Request body.
        :param currency: Currency.
        :param accept_language: Accept language.
        :return: MessageConsequences
        """
        path = "/v2/wallet/emulate"
        params = {"currency": currency}
        headers = {"Accept-Language": accept_language}
        return await self._request(
            method="POST",
            path=path,
            params=params,
            body=body,
            headers=headers,
            response_model=MessageConsequences,
        )

    async def emulate_message_to_account_event(
        self,
        account_id: str,
        body: dict[str, t.Any],
        ignore_signature_check: bool | None = None,
        accept_language: str | None = None,
    ) -> AccountEvent:
        """Emulate sending message to retrieve account-specific events.

        :param account_id: Account ID.
        :param body: Request body.
        :param ignore_signature_check: Ignore signature check.
        :param accept_language: Accept language.
        :return: AccountEvent
        """
        path = f"/v2/accounts/{account_id}/events/emulate"
        params = {"ignore_signature_check": ignore_signature_check}
        headers = {"Accept-Language": accept_language}
        return await self._request(
            method="POST",
            path=path,
            params=params,
            body=body,
            headers=headers,
            response_model=AccountEvent,
        )
