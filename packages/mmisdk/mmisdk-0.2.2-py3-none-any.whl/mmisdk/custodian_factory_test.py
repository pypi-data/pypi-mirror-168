import unittest
from unittest.mock import patch

from mmisdk.adapters.qredo_adapter import QredoAdapter
from mmisdk.custodian_factory import CustodianFactory
from mmisdk.mocks.mock_custodians_config_requests_get import mock_custodians_config_requests_get


class CustodianFactoryTest(unittest.TestCase):

    @patch('requests.get', side_effect=mock_custodians_config_requests_get)
    def test_should_be_defined(self, mock_get):
        factory = CustodianFactory()
        self.assertIsNotNone(factory)

    @patch('requests.get', side_effect=mock_custodians_config_requests_get)
    def test_should_fetch_configs(self, mock_requests):
        factory = CustodianFactory()
        self.assertIsNotNone(factory.custodians_config)
        self.assertGreater(len(factory.custodians_config), 0)

    @patch('requests.get', side_effect=mock_custodians_config_requests_get)
    def test_should_get_supported_custodians(self, mock_requests):
        factory = CustodianFactory()
        supported_custodians = factory.get_supported_custodians()
        self.assertEqual(4, len(supported_custodians))
        self.assertIn("qredo", supported_custodians)
        self.assertIn("qredo-dev", supported_custodians)
        self.assertIn("cactus", supported_custodians)
        self.assertIn("cactus-dev", supported_custodians)

    @patch('requests.get', side_effect=mock_custodians_config_requests_get)
    def test_should_create_custodian(self, mock_requests):
        factory = CustodianFactory()
        custodian = factory.create_for("qredo-dev", "refresh_token")
        self.assertIsNotNone(custodian)
        self.assertIsInstance(custodian, QredoAdapter)

    @patch('requests.get', side_effect=mock_custodians_config_requests_get)
    def test_should_fail_unsupported_custodian(self, mock_requests):
        factory = CustodianFactory()
        with self.assertRaises(AssertionError):
            factory.create_for("whatever", "refresh_token")


if __name__ == "__main__":
    unittest.main()
