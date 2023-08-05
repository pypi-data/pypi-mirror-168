import asyncio
import unittest
from cool_open_client.cool_automation_client import CoolAutomationClient


class CoolAutomationClientTest(unittest.TestCase):
    def setUp(self):
        self.token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYxZjhkYmFlYThhMzFjMTk2NmIxZWNlYyIsImlhdCI6MTY0OTc2MDQxNiwiZXhwIjoxNjgxMzE4MDE2fQ.RLwz3qiZgLBRwHYpPQGrYtPC3t34axQBh2C7pP_wdVU"
        self.loop = asyncio.get_event_loop()
        self.client = self.loop.run_until_complete(CoolAutomationClient.create(token=self.token))

    def test_client_call(self):
        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(CoolAutomationClient.authenticate(username="a", password="aaa"))
        # response = await CoolAutomationClient.authenticate(username="aa", password="aaa")
        print(response)

    def test_get_devices(self):
        response = self.loop.run_until_complete(self.client.get_devices())
        print(response)

    def test_get_units(self):
        response = self.loop.run_until_complete(self.client.get_controllable_units())
        print(response)

    def test_get_me(self):
        response = self.loop.run_until_complete(self.client.get_me())
        print(response)

    def test_set_hvac_mode(self):
        mode = "COOL"
        unit_id = "61f8e55b60bf483d1e5aeef6"
        response = self.loop.run_until_complete(self.client.set_operation_mode(mode= mode, unit_id=unit_id))
        print(response)

if __name__ == "__main__":
    unittest.main()
