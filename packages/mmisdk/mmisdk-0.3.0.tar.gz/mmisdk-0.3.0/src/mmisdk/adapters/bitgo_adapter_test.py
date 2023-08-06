
import unittest
from unittest import mock
from mmisdk.adapters.bitgo_adapter import BitgoAdapter

from mmisdk.bitgo.bitgo_client import BitgoClient
from mmisdk.mocks.mock_bitgo_requests_get import mock_bitgo_requests_get
from mmisdk.mocks.mock_bitgo_requests_post import mock_bitgo_requests_post
from mmisdk.mocks.mock_legacy_tx_params import MOCK_LEGACY_TX_PARAMS


class BitgoAdapterTest(unittest.TestCase):
    """Test Class"""
    @classmethod
    def setUpClass(cls):
        client = BitgoClient("http://some-url", "some-refresh-token")
        cls.custodian = BitgoAdapter(client)

    def test_should_be_defined(self):
        self.assertIsNotNone(self.custodian)

    @mock.patch('requests.get', side_effect=mock_bitgo_requests_get)
    def test_should_get_transaction(self, mock_get):
        transaction = self.custodian.get_transaction("95851701-e573-497a-9df8-fbca8bbf80e9")
        self.assertEqual(transaction.id, '95851701-e573-497a-9df8-fbca8bbf80e9')
        self.assertEqual(transaction.type, '1')
        self.assertEqual(transaction.from_, '0xb22505ee2aac7d52d4a218f5877cdbae3bbeec75')
        self.assertEqual(transaction.to, '0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506')
        self.assertEqual(transaction.value, '1000000000000000000')
        self.assertEqual(transaction.gas, '260849')
        self.assertEqual(transaction.gasPrice, None)
        self.assertEqual(transaction.maxPriorityFeePerGas, None)
        self.assertEqual(transaction.maxFeePerGas, None)
        self.assertEqual(transaction.nonce, None)
        self.assertEqual(transaction.data, "0x7ff36ab500000000000000000000000000000000000000000000000006d5dbf25e950f2f0000000000000000000000000000000000000000000000000000000000000080000000000000000000000000b22505ee2aac7d52d4a218f5877cdbae3bbeec7500000000000000000000000000000000000000000000000000000000624263dd0000000000000000000000000000000000000000000000000000000000000002000000000000000000000000b4fbf271143f4fbf7b91a5ded31805e42b2208d60000000000000000000000001f9840a85d5af5bf1d1762f925bdaddc4201f984")
        self.assertEqual(transaction.hash, "0x2b81204f61c7736cb4b9cf89b842d44081b476f35e521fb745d8e212c02b77b4")
        self.assertEqual(transaction.status.finished, False)
        self.assertEqual(transaction.status.signed, False)
        self.assertEqual(transaction.status.success, False)
        self.assertEqual(transaction.status.displayText, "Created")
        self.assertEqual(transaction.status.reason, "Unknown")

    def test_get_transactions_should_raise(self):
        with self.assertRaises(NotImplementedError):
            self.custodian.get_transactions("some-id")

    @mock.patch('requests.post', side_effect=mock_bitgo_requests_post)
    def test_should_create_transaction(self, mock_post):
        extra_params = {
            "walletId": "someWalletId",
        }
        transaction = self.custodian.create_transaction(MOCK_LEGACY_TX_PARAMS, extra_params)
        self.assertEqual(transaction.id, '6ca20474-f1e6-4f1f-8123-56ff097a06cd')
        self.assertEqual(transaction.type, '1')
        self.assertEqual(transaction.from_, '0xeddb59689e4ec3931b8d42d615c0d4a7a3a208e7')
        self.assertEqual(transaction.to, '0xb22505ee2aac7d52d4a218f5877cdbae3bbeec75')
        self.assertEqual(transaction.value, '999000000')
        self.assertEqual(transaction.gas, '300000')
        self.assertEqual(transaction.gasPrice, None)
        self.assertEqual(transaction.maxPriorityFeePerGas, None)
        self.assertEqual(transaction.maxFeePerGas, None)
        self.assertEqual(transaction.nonce, None)
        self.assertEqual(transaction.data, "0x1111111111111111")
        self.assertEqual(transaction.hash, None)
        self.assertEqual(transaction.status.finished, False)
        self.assertEqual(transaction.status.signed, False)
        self.assertEqual(transaction.status.success, False)
        self.assertEqual(transaction.status.displayText, "Created")
        self.assertEqual(transaction.status.reason, "Unknown")


if __name__ == "__main__":
    unittest.main()
