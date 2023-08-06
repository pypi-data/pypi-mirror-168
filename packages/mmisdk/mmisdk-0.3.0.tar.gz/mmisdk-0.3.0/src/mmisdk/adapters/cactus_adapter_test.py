import unittest
from unittest import mock

from mmisdk.adapters.cactus_adapter import CactusAdapter
from mmisdk.cactus.cactus_client import CactusClient
from mmisdk.mocks.mock_cactus_requests_get import mock_cactus_requests_get
from mmisdk.mocks.mock_cactus_requests_post import mock_cactus_requests_post
from mmisdk.mocks.mock_legacy_tx_params import MOCK_LEGACY_TX_PARAMS


class CactusAdapterTest(unittest.TestCase):
    """Test Class"""
    @classmethod
    def setUpClass(cls):
        client = CactusClient("http://some-url", "some-refresh-token")
        cls.custodian = CactusAdapter(client)

    def test_should_be_defined(self):
        self.assertIsNotNone(self.custodian)

    @mock.patch('requests.get', side_effect=mock_cactus_requests_get)
    @mock.patch('requests.post', side_effect=mock_cactus_requests_post)
    def test_should_get_transaction(self, mock_get, mock_post):
        transaction = self.custodian.get_transaction("VURKJPZ2JVD888888000277")
        self.assertEqual(transaction.id, 'VURKJPZ2JVD888888000277')

    @mock.patch('requests.get', side_effect=mock_cactus_requests_get)
    @mock.patch('requests.post', side_effect=mock_cactus_requests_post)
    def test_should_get_transactions(self, mock_get, mock_post):
        transactions = self.custodian.get_transactions(42)
        self.assertEqual(transactions[0].id, "VURKJPZ2JVD888888000277")
        self.assertEqual(transactions[1].id, "VHV3LIBLVND888888000431")

    @mock.patch('requests.post', side_effect=mock_cactus_requests_post)
    def test_should_create_transaction(self, mock_post):
        extra_params = {
            "chainId": "1",
        }
        transaction = self.custodian.create_transaction(MOCK_LEGACY_TX_PARAMS, extra_params)
        self.assertEqual(transaction.id, 'VHV3LIBLVND888888000431')


if __name__ == "__main__":
    unittest.main()
