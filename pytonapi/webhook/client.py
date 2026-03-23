from __future__ import annotations

import typing as t

import aiohttp

from pytonapi.client import BaseClient
from pytonapi.exceptions import TONAPINotFoundError
from pytonapi.types import (
    DEFAULT_RETRY_POLICY,
    WEBHOOK_BASE_URLS,
    Network,
    RetryPolicy,
)
from pytonapi.webhook.models import (
    AccountSubscription,
    WebhookInfo,
)

if t.TYPE_CHECKING:
    import builtins


class TonapiWebhookClient(BaseClient):
    """Async client for the TONAPI TonapiWebhooks API."""

    def __init__(
        self,
        api_key: str,
        network: Network,
        *,
        base_url: str | None = None,
        timeout: float = 10.0,
        session: aiohttp.ClientSession | None = None,
        headers: dict[str, str] | None = None,
        cookies: dict[str, str] | None = None,
        retry_policy: RetryPolicy | None = DEFAULT_RETRY_POLICY,
    ) -> None:
        """Initialize the TONAPI TonapiWebhooks client.

        :param api_key: TONAPI key. Get one at https://tonconsole.com/.
        :param network: Target network (``Network.MAINNET`` or ``Network.TESTNET``).
        :param base_url: Custom base URL (overrides ``network``).
        :param timeout: Request timeout in seconds.
        :param session: Optional external ``aiohttp.ClientSession``.
            When provided, the client will not close it — the caller
            is responsible for managing its lifecycle.
        :param headers: Additional HTTP headers sent with every request.
        :param cookies: Additional cookies sent with every request.
        :param retry_policy: Retry policy, or ``None`` to disable retries.
        """
        super().__init__(
            api_key=api_key,
            base_url=base_url or WEBHOOK_BASE_URLS[network],
            timeout=timeout,
            session=session,
            headers=headers,
            cookies=cookies,
            retry_policy=retry_policy,
        )

    async def create(self, endpoint: str) -> TonapiWebhook:
        """Create a new webhook.

        :param endpoint: Callback URL for receiving events.
        :return: Bound ``TonapiWebhook`` object.
        """
        data = await self.request(
            "POST",
            "/webhooks",
            body={"endpoint": endpoint},
        )
        return TonapiWebhook(self, data["webhook_id"], endpoint, data["token"])

    async def list(self) -> builtins.list[WebhookInfo]:
        """List all configured webhooks.

        :return: List of ``WebhookInfo`` objects.
        """
        data = await self.request("GET", "/webhooks")
        return [WebhookInfo.model_validate(w) for w in data.get("webhooks", [])]

    async def delete(self, webhook_id: int) -> None:
        """Delete a webhook and all its subscriptions.

        :param webhook_id: TonapiWebhook identifier.
        """
        await self.request("DELETE", f"/webhooks/{webhook_id}")

    async def get_info(self, webhook_id: int) -> WebhookInfo:
        """Fetch full webhook information by ID.

        :param webhook_id: TonapiWebhook identifier.
        :return: ``WebhookInfo`` with current status and subscription counts.
        """
        webhooks = await self.list()
        for w in webhooks:
            if w.id == webhook_id:
                return w
        raise TONAPINotFoundError(
            status=404,
            message=f"TonapiWebhook {webhook_id} not found",
        )

    async def get(self, webhook_id: int) -> TonapiWebhook:
        """Get a bound ``TonapiWebhook`` object by ID.

        :param webhook_id: TonapiWebhook identifier.
        :return: Bound ``TonapiWebhook`` object.
        """
        info = await self.get_info(webhook_id)
        return TonapiWebhook(self, info.id, info.endpoint, info.token)

    async def ensure(self, endpoint: str) -> TonapiWebhook:
        """Find an existing webhook by endpoint or create a new one.

        :param endpoint: Callback URL for receiving events.
        :return: Bound ``TonapiWebhook`` object.
        """
        webhooks = await self.list()
        for w in webhooks:
            if w.endpoint == endpoint:
                return TonapiWebhook(self, w.id, w.endpoint, w.token)
        return await self.create(endpoint)


class TonapiWebhook:
    """Bound webhook object with methods that do not require an explicit ID."""

    def __init__(
        self,
        client: TonapiWebhookClient,
        webhook_id: int,
        endpoint: str,
        token: str,
    ) -> None:
        """Initialize the bound webhook.

        :param client: Parent ``TonapiWebhookClient`` client.
        :param webhook_id: TonapiWebhook identifier.
        :param endpoint: Callback URL.
        :param token: Secret token for ``Authorization`` header verification.
        """
        self._client = client
        self.id = webhook_id
        self.endpoint = endpoint
        self.token = token

    async def subscribe(
        self,
        accounts: list[str],
    ) -> None:
        """Subscribe to account transactions.

        :param accounts: List of account IDs to subscribe to.
        """
        await self._client.request(
            "POST",
            f"/webhooks/{self.id}/account-tx/subscribe",
            body={"accounts": [{"account_id": a} for a in accounts]},
        )

    async def unsubscribe(
        self,
        accounts: list[str],
    ) -> None:
        """Unsubscribe from account transactions.

        :param accounts: List of account IDs to unsubscribe from.
        """
        await self._client.request(
            "POST",
            f"/webhooks/{self.id}/account-tx/unsubscribe",
            body={"accounts": accounts},
        )

    async def get_subscriptions(
        self,
        offset: int = 0,
        limit: int = 10,
    ) -> list[AccountSubscription]:
        """Get account transaction subscriptions for this webhook.

        :param offset: Pagination offset.
        :param limit: Maximum number of results.
        :return: List of ``AccountSubscription`` objects.
        """
        data = await self._client.request(
            "GET",
            f"/webhooks/{self.id}/account-tx/subscriptions",
            params={"offset": offset, "limit": limit},
        )
        return [
            AccountSubscription.model_validate(s)
            for s in data.get("account_tx_subscriptions", [])
        ]

    async def subscribe_new_contracts(self) -> None:
        """Subscribe to events about new contract deployments."""
        await self._client.request(
            "POST",
            f"/webhooks/{self.id}/subscribe-new-contracts",
        )

    async def unsubscribe_new_contracts(self) -> None:
        """Unsubscribe from events about new contract deployments."""
        await self._client.request(
            "POST",
            f"/webhooks/{self.id}/unsubscribe-new-contracts",
        )

    async def subscribe_mempool_msg(self) -> None:
        """Subscribe to mempool events."""
        await self._client.request(
            "POST",
            f"/webhooks/{self.id}/mempool/subscribe",
        )

    async def unsubscribe_mempool_msg(self) -> None:
        """Unsubscribe from mempool events."""
        await self._client.request(
            "POST",
            f"/webhooks/{self.id}/mempool/unsubscribe",
        )

    async def subscribe_opcode_msg(self, opcode: str) -> None:
        """Subscribe to messages with a specific opcode.

        :param opcode: Opcode in hex format (``0x`` prefix).
        """
        await self._client.request(
            "POST",
            f"/webhooks/{self.id}/subscribe-msg-opcode/{opcode}",
        )

    async def unsubscribe_opcode_msg(self, opcode: str) -> None:
        """Unsubscribe from messages with a specific opcode.

        :param opcode: Opcode in hex format (``0x`` prefix).
        """
        await self._client.request(
            "POST",
            f"/webhooks/{self.id}/unsubscribe-msg-opcode/{opcode}",
        )

    async def sync_accounts(
        self,
        accounts: list[str],
    ) -> None:
        """Sync account subscriptions — subscribe missing, unsubscribe extra.

        :param accounts: Desired list of account IDs.
        """
        current_subs = await self._get_all_subscriptions()
        current = frozenset(s.account_id for s in current_subs)
        desired = frozenset(accounts)

        to_add = desired - current
        to_remove = current - desired

        if to_add:
            await self.subscribe(list(to_add))
        if to_remove:
            await self.unsubscribe(list(to_remove))

    async def _get_all_subscriptions(self) -> list[AccountSubscription]:
        """Fetch all account subscriptions using pagination.

        :return: Complete list of ``AccountSubscription`` objects.
        """
        all_subs: list[AccountSubscription] = []
        offset = 0
        limit = 100
        while True:
            batch = await self.get_subscriptions(offset=offset, limit=limit)
            all_subs.extend(batch)
            if len(batch) < limit:
                break
            offset += limit
        return all_subs

    async def delete(self) -> None:
        """Delete this webhook and all its subscriptions."""
        await self._client.delete(self.id)
