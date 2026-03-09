from pytonapi.webhook import AccountSubscription, TonapiWebhook, WebhookInfo
from tests.conftest import TestTonapiWebhook

ACCOUNT_ID = "0:408da3b28b6c065a593e10391269baaa9c5f8caebc0c69d9f0aabbab2a99256b"


class TestTonapiWebhookClient(TestTonapiWebhook):
    async def test_create_get_and_delete(self):
        webhook = await self.webhook.create("https://example.com/test-hook")
        self.assertIsInstance(webhook, TonapiWebhook)
        self.assertIsInstance(webhook.id, int)
        self.assertEqual(webhook.endpoint, "https://example.com/test-hook")

        fetched = await self.webhook.get(webhook.id)
        self.assertEqual(fetched.id, webhook.id)
        self.assertEqual(fetched.endpoint, webhook.endpoint)

        await webhook.delete()

    async def test_list(self):
        response = await self.webhook.list()
        self.assertIsInstance(response, list)
        for item in response:
            self.assertIsInstance(item, WebhookInfo)

    async def test_ensure_idempotent(self):
        webhook = await self.webhook.ensure("https://example.com/ensure-hook")
        self.assertIsInstance(webhook, TonapiWebhook)

        same = await self.webhook.ensure("https://example.com/ensure-hook")
        self.assertEqual(webhook.id, same.id)

        await webhook.delete()

    async def test_subscribe_and_unsubscribe(self):
        webhook = await self.webhook.create("https://example.com/sub-hook")

        await webhook.subscribe([ACCOUNT_ID])
        subscriptions = await webhook.get_subscriptions()
        self.assertIsInstance(subscriptions, list)
        for item in subscriptions:
            self.assertIsInstance(item, AccountSubscription)

        await webhook.unsubscribe([ACCOUNT_ID])
        await webhook.delete()
