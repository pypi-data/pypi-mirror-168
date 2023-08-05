import asyncio
import unittest

from cool_open_client.hvac_units_factory import HVACUnitsFactory


class TestHvacUnitsFactory(unittest.TestCase):
    def setUp(self):
        self.token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYxZjhkYmFlYThhMzFjMTk2NmIxZWNlYyIsImlhdCI6MTY0OTc2MDQxNiwiZXhwIjoxNjgxMzE4MDE2fQ.RLwz3qiZgLBRwHYpPQGrYtPC3t34axQBh2C7pP_wdVU"
        self.loop = asyncio.get_event_loop()

    def test_get_units(self):
        factory = self.loop.run_until_complete(HVACUnitsFactory.create(self.token))
        units = self.loop.run_until_complete(factory.generate_units_from_api())
        assert units is not None


if __name__ == "__main__":
    unittest.main()
