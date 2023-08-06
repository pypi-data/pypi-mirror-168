import requests

import unittest
from unittest import mock
from mmisdk.bitgo.bitgo_client import BitgoClient
from mmisdk.bitgo.bitgo_create_tx_params import BitgoCreateTxParams
from mmisdk.mocks.mock_bitgo_requests_get import mock_bitgo_requests_get
from mmisdk.mocks.mock_bitgo_requests_post import mock_bitgo_requests_post


class BitgoClientTest(unittest.TestCase):
    """Test Class"""
    @classmethod
    def setUpClass(cls):
        cls.client = BitgoClient("http://some-url", "some-bitgo-jwt-token")

    def test_should_be_defined(self):
        self.assertIsNotNone(self.client)

    def test_should_get_headers(self):
        headers = self.client._BitgoClient__get_headers()
        self.assertEqual(headers, {
            "Content-Type": "application/json",
            "Authorization": 'Bearer some-bitgo-jwt-token'
        })

    @mock.patch('requests.get', side_effect=mock_bitgo_requests_get)
    def test_should_get_transaction(self, mock_get):
        bitgo_list_response = self.client.get_transaction_by_custodian_tx_id("fdee94d9-5e91-447d-ba36-97f42a5c7dc6")

        self.assertIsNotNone(bitgo_list_response.data)
        self.assertEqual(len(bitgo_list_response.data), 1)
        self.assertIsNotNone(bitgo_list_response.meta)

        transaction = bitgo_list_response.data[0]
        print(transaction)
        self.assertEqual(transaction.transactionStatus, "created")
        self.assertEqual(transaction.custodianTransactionId, "95851701-e573-497a-9df8-fbca8bbf80e9")
        self.assertEqual(transaction.from_, "0xb22505ee2aac7d52d4a218f5877cdbae3bbeec75")
        self.assertEqual(transaction.to, "0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506")
        self.assertEqual(transaction.coin, "gteth")
        self.assertEqual(transaction.value, "1000000000000000000")
        self.assertEqual(transaction.gasLimit, "260849")
        self.assertEqual(transaction.userId, "5e822adc91a83a3f00975fa72b5a536d")
        self.assertEqual(transaction.createdTime, "2022-03-29T01:12:10.016Z")
        self.assertEqual(transaction.data, "0x7ff36ab500000000000000000000000000000000000000000000000006d5dbf25e950f2f0000000000000000000000000000000000000000000000000000000000000080000000000000000000000000b22505ee2aac7d52d4a218f5877cdbae3bbeec7500000000000000000000000000000000000000000000000000000000624263dd0000000000000000000000000000000000000000000000000000000000000002000000000000000000000000b4fbf271143f4fbf7b91a5ded31805e42b2208d60000000000000000000000001f9840a85d5af5bf1d1762f925bdaddc4201f984")
        self.assertEqual(transaction.decodedData["protocolName"], "SushiswapV2Router")

    @mock.patch('requests.get', side_effect=mock_bitgo_requests_get)
    def test_should_raise_on_invalid_custodian_tx_id(self, mock_get):
        with self.assertRaises(requests.HTTPError):
            self.client.get_transaction_by_custodian_tx_id("INVALID-CUSTODIAN-TX-ID")

    @mock.patch('requests.post', side_effect=mock_bitgo_requests_post)
    def test_should_create_transaction(self, mock_post):
        wallet_id = "614a2a61df1332000686516a6dbee90a"
        bitgo_create_tx_params = BitgoCreateTxParams(txParams={
            "from_": "0xeddb59689e4ec3931b8d42d615c0d4a7a3a208e7",
            "to": "0xb22505ee2aac7d52d4a218f5877cdbae3bbeec75",
            "value": "999000000",
            "gasPrice": "100",
            "gasLimit": "300000",
            "data": "0x1111111111111111"
        })
        bitgo_response = self.client.create_transaction(wallet_id, bitgo_create_tx_params)

        self.assertIsNotNone(bitgo_response.data)

        transaction = bitgo_response.data
        self.assertEqual(transaction.transactionStatus, "created")
        self.assertEqual(transaction.custodianTransactionId, "6ca20474-f1e6-4f1f-8123-56ff097a06cd")
        self.assertEqual(transaction.from_, "0xeddb59689e4ec3931b8d42d615c0d4a7a3a208e7")
        self.assertEqual(transaction.to, "0xb22505ee2aac7d52d4a218f5877cdbae3bbeec75")
        self.assertEqual(transaction.coin, "gteth")
        self.assertEqual(transaction.gasLimit, "300000")
        self.assertEqual(transaction.value, "999000000")
        self.assertEqual(transaction.data, "0x1111111111111111")
        self.assertEqual(transaction.createdTime, "2022-09-22T08:19:55.843Z")


if __name__ == "__main__":
    unittest.main()
