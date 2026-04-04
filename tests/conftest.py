import asyncio
from unittest import IsolatedAsyncioTestCase

from environs import Env

from pytonapi.rest import TonapiRestClient
from pytonapi.streaming import TonapiStreaming
from pytonapi.types import Network
from pytonapi.webhook import TonapiWebhookClient

env = Env()
env.read_env()

API_KEY = env.str("TONAPI_API_KEY")
NETWORK = Network[env.str("TONAPI_NETWORK", "MAINNET")]
RPS_LIMIT = env.int("TONAPI_RPS_LIMIT")
RPS_PERIOD = env.float("TONAPI_RPS_PERIOD")


class TestTonapiRest(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.tonapi = TonapiRestClient(
            API_KEY,
            NETWORK,
            rps_limit=RPS_LIMIT,
            rps_period=RPS_PERIOD,
        )
        await self.tonapi.create_session()

    async def asyncTearDown(self) -> None:
        await self.tonapi.close_session()


class TestTonapiWebhook(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.webhook = TonapiWebhookClient(
            API_KEY,
            NETWORK,
        )
        await self.webhook.create_session()

    async def asyncTearDown(self) -> None:
        await self.webhook.close_session()


class TestTonapiStreaming(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.streaming = TonapiStreaming(
            API_KEY,
            NETWORK,
        )
        await self.streaming.create_session()

    async def asyncTearDown(self) -> None:
        await self.streaming.close_session()

    @staticmethod
    def make_stop(seconds: float) -> asyncio.Event:
        event = asyncio.Event()

        async def _set_after() -> None:
            await asyncio.sleep(seconds)
            event.set()

        event._task = asyncio.ensure_future(_set_after())  # type: ignore[attr-defined]
        return event
