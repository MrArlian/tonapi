# This file is auto-generated. Do not edit manually.

from pytonapi.rest.models import Event
from tests.conftest import TestTonapiRest
from tests.rest.fixtures import params


class TestEventsResource(TestTonapiRest):
    async def test_get_event(self):
        p = params("events.get_event")
        response = await self.tonapi.events.get_event(
            p["event_id"],
        )
        self.assertIsInstance(response, Event)

    # async def test_emulate_message_to_event(self):
    #     p = params("events.emulate_message_to_event")
    #     response = await self.tonapi.events.emulate_message_to_event(
    #         body=p["body"],
    #     )
    #     self.assertIsInstance(response, Event)
