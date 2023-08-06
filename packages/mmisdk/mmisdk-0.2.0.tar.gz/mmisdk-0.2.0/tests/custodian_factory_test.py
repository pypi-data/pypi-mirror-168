import unittest
from unittest.mock import patch

from mmisdk.custodian_factory import CustodianFactory
from mmisdk.qredo.qredo import Qredo
from mmisdk.utils.mock_response import MockResponse

MOCK_CUSTODIANS_CONFIG = {
    "portfolio": {
        "enabled": True,
        "url": "https://metamask-institutional.io/",
        "cookieSetUrls": [
            "https://mmi-portfolio-poc.codefi.network/api/update-dashboard-cookie",
            "https://metamask-institutional.io/api/update-dashboard-cookie"
        ]
    },
    "custodians": [
        {
            "refreshTokenUrl": None,
            "name": "cactus",
            "displayName": None,
            "enabled": None,
            "mmiApiUrl": "https://mmi.codefi.network/v1",
            "apiBaseUrl": None,
            "iconUrl": None,
            "isNoteToTraderSupported": False
        },
        {
            "refreshTokenUrl": None,
            "name": "qredo",
            "displayName": None,
            "enabled": None,
            "mmiApiUrl": "https://mmi.codefi.network/v1",
            "apiBaseUrl": None,
            "iconUrl": None,
            "isNoteToTraderSupported": True
        },
    ]
}


def mocked_requests_get(*args, **kwargs):
    """ This method will be used by the mock to replace requests.get"""

    # Mock the request that gets the custodian configs
    if args[0].__contains__('/configuration/default'):
        return MockResponse(MOCK_CUSTODIANS_CONFIG, 200)

    return MockResponse(None, 404)


class CustodianFactoryTest(unittest.TestCase):

    @patch('requests.get', side_effect=mocked_requests_get)
    def test_should_be_defined(self, mock_get):
        factory = CustodianFactory()
        self.assertIsNotNone(factory)

    @patch('requests.get', side_effect=mocked_requests_get)
    def test_should_fetch_configs(self, mock_requests):
        factory = CustodianFactory()
        self.assertIsNotNone(factory.custodians_config)
        self.assertGreater(len(factory.custodians_config), 0)

    @patch('requests.get', side_effect=mocked_requests_get)
    def test_should_get_supported_custodians(self, mock_requests):
        factory = CustodianFactory()
        supported_custodians = factory.get_supported_custodians()
        self.assertEqual(4, len(supported_custodians))
        self.assertIn("qredo", supported_custodians)
        self.assertIn("qredo-dev", supported_custodians)
        self.assertIn("cactus", supported_custodians)
        self.assertIn("cactus-dev", supported_custodians)

    @patch('requests.get', side_effect=mocked_requests_get)
    def test_should_create_custodian(self, mock_requests):
        factory = CustodianFactory()
        custodian = factory.create_for("qredo-dev", "refresh_token")
        self.assertIsNotNone(custodian)
        self.assertIsInstance(custodian, Qredo)
        self.assertEqual(custodian.api_url, "https://7ba211-api.qredo.net")
        self.assertEqual(custodian.refresh_token, "refresh_token")

    @patch('requests.get', side_effect=mocked_requests_get)
    def test_should_fail_unsupported_custodian(self, mock_requests):
        factory = CustodianFactory()
        with self.assertRaises(AssertionError):
            factory.create_for("whatever", "refresh_token")


if __name__ == "__main__":
    unittest.main()
