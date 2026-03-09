# This file is auto-generated. Do not edit manually.

from pytonapi.rest.models import Trace
from tests.conftest import TestTonapiRest
from tests.rest.fixtures import params


class TestTracesResource(TestTonapiRest):
    async def test_get_trace(self):
        p = params("traces.get_trace")
        response = await self.tonapi.traces.get_trace(
            p["trace_id"],
        )
        self.assertIsInstance(response, Trace)

    # async def test_emulate_message_to_trace(self):
    #     p = params("traces.emulate_message_to_trace")
    #     response = await self.tonapi.traces.emulate_message_to_trace(
    #         body=p["body"],
    #     )
    #     self.assertIsInstance(response, Trace)
