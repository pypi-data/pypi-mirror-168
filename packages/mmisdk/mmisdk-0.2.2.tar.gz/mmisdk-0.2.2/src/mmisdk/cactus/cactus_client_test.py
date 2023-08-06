import unittest
from unittest import mock

from mmisdk.cactus.cactus_client import CactusClient
from mmisdk.cactus.cactus_get_transactions_params import CactusGetTransactionsParams
from mmisdk.cactus.cactus_tx_params import CactusTXParams
from mmisdk.mocks.mock_cactus_requests_get import mock_cactus_requests_get
from mmisdk.mocks.mock_cactus_requests_post import mock_cactus_requests_post


class CactusClientTest(unittest.TestCase):
    """Test Class"""
    @ classmethod
    def setUpClass(cls):
        cls.client = CactusClient("http://some-url", "some-refresh-token")

    def test_should_be_defined(self):
        self.assertIsNotNone(self.client)

    @mock.patch('requests.post', side_effect=mock_cactus_requests_post)
    def test_should_create_access_token(self, mock_post):
        access_token = self.client._CactusClient__create_access_token()
        self.assertEqual(access_token, "some-access-token")

    @mock.patch('requests.post', side_effect=mock_cactus_requests_post)
    def test_should_get_headers(self, mock_post):
        headers = self.client._CactusClient__get_headers()
        self.assertEqual(headers, {
            "Content-Type": "application/json",
            "Authorization": 'Bearer some-access-token'
        })

    @mock.patch('requests.get', side_effect=mock_cactus_requests_get)
    @mock.patch('requests.post', side_effect=mock_cactus_requests_post)
    def test_should_get_transaction(self, mock_get, mock_post):
        params = CactusGetTransactionsParams(chainId=42, transactionId="VURKJPZ2JVD888888000277")
        results = self.client.get_transactions(params)
        cactus_transaction_detail_1 = results[0]
        cactus_transaction_detail_2 = results[1]

        self.assertEqual(cactus_transaction_detail_1.transactionStatus, "completed")
        self.assertEqual(cactus_transaction_detail_1.transactionHash, "0x27a8aa70a501c20c7614aac084add4482482b51447804ff23275b1fb21e63927")
        self.assertEqual(cactus_transaction_detail_1.custodian_transactionId, "VURKJPZ2JVD888888000277")
        self.assertEqual(cactus_transaction_detail_1.gasPrice, "1000000007")
        self.assertEqual(cactus_transaction_detail_1.maxFeePerGas, "1400000012")
        self.assertEqual(cactus_transaction_detail_1.maxPriorityFeePerGas, "1000000008")
        self.assertEqual(cactus_transaction_detail_1.gasLimit, "180549")
        self.assertEqual(cactus_transaction_detail_1.nonce, "0")
        self.assertEqual(cactus_transaction_detail_1.from_, "0xA7f5D02E141c5DF8A987833E01E4f0922A91cF29")
        self.assertEqual(cactus_transaction_detail_1.signature, None)

        self.assertEqual(cactus_transaction_detail_2.transactionStatus, "completed")
        self.assertEqual(cactus_transaction_detail_2.transactionHash, "0xc062e8e89fa6447b59fc981fa6be352d012bd8bf92bb6833626bcb34c89ce455")
        self.assertEqual(cactus_transaction_detail_2.custodian_transactionId, "VHV3LIBLVND888888000431")
        self.assertEqual(cactus_transaction_detail_2.gasPrice, "1000000008")
        self.assertEqual(cactus_transaction_detail_2.maxFeePerGas, "3500000012")
        self.assertEqual(cactus_transaction_detail_2.maxPriorityFeePerGas, "1000000000")
        self.assertEqual(cactus_transaction_detail_2.gasLimit, "1500000")
        self.assertEqual(cactus_transaction_detail_2.nonce, "4")
        self.assertEqual(cactus_transaction_detail_2.from_, "0xA7f5D02E141c5DF8A987833E01E4f0922A91cF29")
        self.assertEqual(cactus_transaction_detail_2.signature, None)

    @ mock.patch('requests.get', side_effect=mock_cactus_requests_get)
    @ mock.patch('requests.post', side_effect=mock_cactus_requests_post)
    def test_should_get_transactions(self, mock_get, mock_post):
        cactus_get_transactions_params = CactusGetTransactionsParams(
            chainId=42,
        )
        transactions = self.client.get_transactions(cactus_get_transactions_params)
        tx0 = transactions[0]
        self.assertEqual(tx0.transactionStatus, "completed")
        self.assertEqual(tx0.transactionHash, "0x27a8aa70a501c20c7614aac084add4482482b51447804ff23275b1fb21e63927")
        self.assertEqual(tx0.custodian_transactionId, "VURKJPZ2JVD888888000277")
        self.assertEqual(tx0.gasPrice, "1000000007")
        self.assertEqual(tx0.maxFeePerGas, "1400000012")
        self.assertEqual(tx0.maxPriorityFeePerGas, "1000000008")
        self.assertEqual(tx0.gasLimit, "180549")
        self.assertEqual(tx0.nonce, "0")
        self.assertEqual(tx0.from_, "0xA7f5D02E141c5DF8A987833E01E4f0922A91cF29")
        self.assertEqual(tx0.signature, None)

        tx1 = transactions[1]
        self.assertEqual(tx1.transactionStatus, "completed")
        self.assertEqual(tx1.transactionHash, "0xc062e8e89fa6447b59fc981fa6be352d012bd8bf92bb6833626bcb34c89ce455")
        self.assertEqual(tx1.custodian_transactionId, "VHV3LIBLVND888888000431")
        self.assertEqual(tx1.gasPrice, "1000000008")
        self.assertEqual(tx1.maxFeePerGas, "3500000012")
        self.assertEqual(tx1.maxPriorityFeePerGas, "1000000000")
        self.assertEqual(tx1.gasLimit, "1500000")
        self.assertEqual(tx1.nonce, "4")
        self.assertEqual(tx1.from_, "0xA7f5D02E141c5DF8A987833E01E4f0922A91cF29")
        self.assertEqual(tx1.from_, "0xA7f5D02E141c5DF8A987833E01E4f0922A91cF29")
        self.assertEqual(tx1.signature, None)

    @mock.patch('requests.post', side_effect=mock_cactus_requests_post)
    def test_should_create_transaction(self, mock_post):
        """We mock the methods requests.get and requests.post via the above decorators"""
        chain_id = 42
        cactus_tx_params = CactusTXParams(
            from_="0xA7f5D02E141c5DF8A987833E01E4f0922A91cF29",
            to="0xF4312f38f1139C2aa1c1dA54EF38F9ef1628dcB9",
            gasLimit="1500000",
            value="10000",
            data="",
            gasPrice="1000000008",
            maxFeePerGas=None,
            maxPriorityFeePerGas=None
        )
        cactus_transaction_detail = self.client.create_transaction(chain_id, cactus_tx_params)
        self.assertEqual(cactus_transaction_detail.custodian_transactionId, 'VHV3LIBLVND888888000431')


if __name__ == "__main__":
    unittest.main()
