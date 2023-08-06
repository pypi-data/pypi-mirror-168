import unittest
from unittest import mock
from mmisdk.cactus.cactus import Cactus
from mmisdk.utils.mock_response import MockResponse

MOCK_TRANSACTION_1 = {
    "chain_id": "42",
    "nonce": "0",
    "from": "0xA7f5D02E141c5DF8A987833E01E4f0922A91cF29",
    "signature": None,
    "transactionStatus": "completed",
    "transactionHash": "0x27a8aa70a501c20c7614aac084add4482482b51447804ff23275b1fb21e63927",
    "custodian_transactionId": "VURKJPZ2JVD888888000277",
    "gasPrice": "1000000007",
    "maxFeePerGas": "1400000012",
    "maxPriorityFeePerGas": "1000000008",
    "gasLimit": "180549"
}

MOCK_TRANSACTION_2 = {
    "chain_id": "42",
    "nonce": "4",
    "from": "0xA7f5D02E141c5DF8A987833E01E4f0922A91cF29",
    "signature": None,
    "transactionStatus": "completed",
    "transactionHash": "0xc062e8e89fa6447b59fc981fa6be352d012bd8bf92bb6833626bcb34c89ce455",
    "custodian_transactionId": "VHV3LIBLVND888888000431",
    "gasPrice": "1000000008",
    "maxFeePerGas": "3500000012",
    "maxPriorityFeePerGas": "1000000000",
    "gasLimit": "1500000"
}


def mocked_requests_get(*args, **kwargs):
    """ This method will be used by the mock to replace requests.get"""
    # Mock the request that gets all transactions
    if args[0].__contains__('/transactions'):
        return MockResponse([MOCK_TRANSACTION_1, MOCK_TRANSACTION_2], 200)

    return MockResponse(None, 404)


def mocked_requests_post(*args, **kwargs):
    """ This method will be used by the mock to replace requests.post"""

    # Mock the request that creates the access token
    if args[0].__contains__('/tokens'):
        return MockResponse({"jwt": "some-access-token"}, 200)

    # Mock the request that creates a transaction
    if args[0].__contains__('/transactions'):
        return MockResponse(MOCK_TRANSACTION_2, 200)

    return MockResponse(None, 404)


class CactusTest(unittest.TestCase):
    """Test Class"""
    @classmethod
    def setUpClass(cls):
        cls.custodian = Cactus("http://some-url", "some-refresh-token")

    def test_should_be_defined(self):
        self.assertIsNotNone(self.custodian)

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_should_create_access_token(self, mock_post):
        access_token = self.custodian._Cactus__create_access_token()
        self.assertEqual(access_token, "some-access-token")

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_should_get_headers(self, mock_post):
        headers = self.custodian._Cactus__get_headers()
        self.assertEqual(headers, {
            "Content-Type": "application/json",
            "Authorization": 'Bearer some-access-token'
        })

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_should_get_transaction(self, mock_get, mock_post):
        tx = self.custodian.get_transaction("VURKJPZ2JVD888888000277", 42)
        self.assertEqual(tx.id, "VURKJPZ2JVD888888000277")
        self.assertEqual(tx.type, "1")
        self.assertEqual(tx.from_, "0xA7f5D02E141c5DF8A987833E01E4f0922A91cF29")
        self.assertEqual(tx.to, None)
        self.assertEqual(tx.gas, "180549")
        self.assertEqual(tx.gasPrice, "1000000007")
        self.assertEqual(tx.maxFeePerGas, "1400000012")
        self.assertEqual(tx.maxPriorityFeePerGas, "1000000008")
        self.assertEqual(tx.nonce, "0")
        self.assertEqual(tx.data, None)
        self.assertEqual(tx.hash, "0x27a8aa70a501c20c7614aac084add4482482b51447804ff23275b1fb21e63927")
        self.assertEqual(tx.status, {
            "finished": True,
            "submitted": True,
            "signed": True,
            "success": False,
            "displayText": 'Completed',
            "reason": "Unknown",
        })

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_should_get_transaction_no_chain_id(self, mock_get, mock_post):
        self.custodian.get_transaction("VURKJPZ2JVD888888000277")

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_should_get_transactions(self, mock_get, mock_post):
        transactions = self.custodian.get_transactions(42)
        tx0 = transactions[0]
        self.assertEqual(tx0.id, "VURKJPZ2JVD888888000277")
        self.assertEqual(tx0.type, "1")
        self.assertEqual(tx0.from_, "0xA7f5D02E141c5DF8A987833E01E4f0922A91cF29")
        self.assertEqual(tx0.to, None)
        self.assertEqual(tx0.gas, "180549")
        self.assertEqual(tx0.gasPrice, "1000000007")
        self.assertEqual(tx0.maxFeePerGas, "1400000012")
        self.assertEqual(tx0.maxPriorityFeePerGas, "1000000008")
        self.assertEqual(tx0.nonce, "0")
        self.assertEqual(tx0.data, None)
        self.assertEqual(tx0.hash, "0x27a8aa70a501c20c7614aac084add4482482b51447804ff23275b1fb21e63927")
        self.assertEqual(tx0.status, {
            "finished": True,
            "submitted": True,
            "signed": True,
            "success": False,
            "displayText": 'Completed',
            "reason": "Unknown",
        })

        tx1 = transactions[1]
        self.assertEqual(tx1.id, "VHV3LIBLVND888888000431")
        self.assertEqual(tx1.type, "1")
        self.assertEqual(tx1.from_, "0xA7f5D02E141c5DF8A987833E01E4f0922A91cF29")
        self.assertEqual(tx1.to, None)
        self.assertEqual(tx1.gas, "1500000")
        self.assertEqual(tx1.gasPrice, "1000000008")
        self.assertEqual(tx1.maxFeePerGas, "3500000012")
        self.assertEqual(tx1.maxPriorityFeePerGas, "1000000000")
        self.assertEqual(tx1.nonce, "4")
        self.assertEqual(tx1.data, None)
        self.assertEqual(tx1.hash, "0xc062e8e89fa6447b59fc981fa6be352d012bd8bf92bb6833626bcb34c89ce455")
        self.assertEqual(tx1.status, {
            "finished": True,
            "submitted": True,
            "signed": True,
            "success": False,
            "displayText": 'Completed',
            "reason": "Unknown",
        })

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_should_get_transactions_no_chain_id(self, mock_get, mock_post):
        self.custodian.get_transactions()

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_should_create_transaction(self, mock_post):
        """We mock the methods requests.get and requests.post via the above decorators"""
        tx_params = {
            "from": "0xA7f5D02E141c5DF8A987833E01E4f0922A91cF29",
            "to": "0xF4312f38f1139C2aa1c1dA54EF38F9ef1628dcB9",
            "value": None,
            "data": None,
            "gasLimit": "1500000",
            "gas": "1000000008",
            "nonce": 4,
            "type": "1",
            "gasPrice": "1000000008"
        }
        extra_params = {
            "chainId": "42",
            "note": "Some note"
        }
        transaction = self.custodian.create_transaction(tx_params, extra_params)
        self.assertEqual(transaction.id, 'VHV3LIBLVND888888000431')


if __name__ == "__main__":
    unittest.main()
