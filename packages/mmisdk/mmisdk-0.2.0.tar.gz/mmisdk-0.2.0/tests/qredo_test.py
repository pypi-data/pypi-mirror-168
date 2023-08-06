import requests
import unittest
from unittest import mock

from mmisdk.qredo.qredo import Qredo
from mmisdk.utils.mock_response import MockResponse

MOCK_TRANSACTION = {
    "txID": "2ELuLA4HWIzPBQB1MSLmbOxtoB1",
    "txHash": "0x6b5dc3519b325be4e6f9512f8d3b1fdb7af22a996e3f6bb1a898a28ef05c1963",
    "status": "authorized",
    "timestamps": {
        "authorized": 1662387127,
        "created": 1662387126
    },
    "events": [{
        "id": "2ELuLAcfbNcFqCmYPHlaGlkIdQf",
        "timestamp": 1662387126,
        "status": "created",
        "message": ""
    },
        {
        "id": "2ELuLBuOP6tc1Pp09FSHKvfvOoZ",
        "timestamp": 1662387127,
        "status": "authorized",
        "message": ""
    }],
    "nonce": 0,
    "gasPrice": "1000",
    "gasLimit": "21000",
    "from": "0x62468FD916bF27A3b76d3de2e5280e53078e13E1",
    "to":   "0x9999999999999999999999999999999999999999",
    "value": "1",
    "data": "",
    "rawTX": "4YCCA-iCUgiUYkaP2Ra_J6O3bT3i5SgOUweOE-EBgICAgA",
    "createdBy": "EFvSMt9uGTEsDCx22sYB8BPz1bCyxAZNPKDWpJVsLKM9",
    "accountID": "2ECrNK9dUlYIpdI4xVuRQ4Diuwq",
    "network": "",
    "chainID": "1"
}


def mocked_requests_get(*args, **kwargs):
    """ This method will be used by the mock to replace requests.get"""

    # Mock the request that gets the transaction
    if args[0].__contains__('/connect/transaction'):
        return MockResponse(MOCK_TRANSACTION, 200)

    return MockResponse(None, 404)


def mocked_requests_post(*args, **kwargs):
    """ This method will be used by the mock to replace requests.post"""

    # Mock the request that creates the access token
    if args[0].__contains__('/connect/token'):
        return MockResponse({"access_token": "some-access-token"}, 200)

    # Mock the request that creates a transaction
    if args[0].__contains__('/connect/transaction'):
        return MockResponse(MOCK_TRANSACTION, 200)

    return MockResponse(None, 404)


class QredoTest(unittest.TestCase):
    """Test Class"""
    @classmethod
    def setUpClass(cls):
        cls.custodian = Qredo("http://some-url", "some-refresh-token")

    def test_should_be_defined(self):
        self.assertIsNotNone(self.custodian)

    def test_should_get_transactions(self):
        with self.assertRaises(requests.HTTPError):
            self.custodian.get_transactions(1)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_should_get_transaction(self, mock_get, mock_post):
        """We mock the methods requests.get and requests.post via the above decorators"""

        transaction = self.custodian.get_transaction(
            "2ELuLA4HWIzPBQB1MSLmbOxtoB1")
        self.assertEqual(transaction.id, '2ELuLA4HWIzPBQB1MSLmbOxtoB1')
        self.assertEqual(transaction.type, '1')
        self.assertEqual(transaction.from_,
                         '0x62468FD916bF27A3b76d3de2e5280e53078e13E1')
        self.assertEqual(
            transaction.to, '0x9999999999999999999999999999999999999999')
        self.assertEqual(transaction.value, '1')
        self.assertEqual(transaction.gas, '21000')
        self.assertEqual(transaction.gasPrice, '1000')
        self.assertEqual(transaction.maxPriorityFeePerGas, None)
        self.assertEqual(transaction.maxFeePerGas, None)
        self.assertEqual(transaction.nonce, '0')
        self.assertEqual(
            transaction.hash, '0x6b5dc3519b325be4e6f9512f8d3b1fdb7af22a996e3f6bb1a898a28ef05c1963')
        self.assertEqual(transaction.status, {
            "finished": False,
            "submitted": False,
            "signed": False,
            "success": False,
            "displayText": 'Authorized',
            "reason": "Unknown",
        })

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_should_create_transaction(self, mock_post):
        """We mock the methods requests.get and requests.post via the above decorators"""
        tx_params = {
            "from": "0x62468FD916bF27A3b76d3de2e5280e53078e13E1",
            "to": "0x9999999999999999999999999999999999999999",
            "value": "1",
            "data": "",
            "gasLimit": "21000",
            "gas": "1000",
            "nonce": 0,
            "type": "1",
            "gasPrice": "1000"
        }
        extra_params = {
            "chainId": "1",
            "note": "Some note"
        }
        transaction = self.custodian.create_transaction(tx_params, extra_params)
        self.assertEqual(transaction.id, '2ELuLA4HWIzPBQB1MSLmbOxtoB1')


if __name__ == "__main__":
    unittest.main()
