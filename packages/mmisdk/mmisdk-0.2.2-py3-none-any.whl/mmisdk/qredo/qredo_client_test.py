import unittest
from unittest import mock

from mmisdk.mocks.mock_qredo_requests_get import mock_qredo_requests_get
from mmisdk.mocks.mock_qredo_requests_post import mock_qredo_requests_post
from mmisdk.qredo.qredo_client import QredoClient
from mmisdk.qredo.qredo_new_transaction import QredoNewTransaction
from mmisdk.qredo.qredo_transaction_info import QredoTransactionStatus


class QredoClientTest(unittest.TestCase):
    """Test Class"""
    @classmethod
    def setUpClass(cls):
        cls.client = QredoClient("http://some-url", "some-refresh-token")

    def test_should_be_defined(self):
        self.assertIsNotNone(self.client)

    @mock.patch('requests.get', side_effect=mock_qredo_requests_get)
    @mock.patch('requests.post', side_effect=mock_qredo_requests_post)
    def test_should_get_transaction(self, mock_get, mock_post):
        """We mock the methods requests.get and requests.post via the above decorators"""

        qredo_transaction_info = self.client.get_transaction(
            "2ELuLA4HWIzPBQB1MSLmbOxtoB1")
        self.assertEqual(qredo_transaction_info.txID, '2ELuLA4HWIzPBQB1MSLmbOxtoB1')
        self.assertEqual(qredo_transaction_info.txHash, '0x6b5dc3519b325be4e6f9512f8d3b1fdb7af22a996e3f6bb1a898a28ef05c1963')
        self.assertEqual(qredo_transaction_info.status, QredoTransactionStatus.AUTHORIZED)
        self.assertEqual(qredo_transaction_info.nonce, 0)
        self.assertEqual(qredo_transaction_info.from_,
                         '0x62468FD916bF27A3b76d3de2e5280e53078e13E1')
        self.assertEqual(
            qredo_transaction_info.to, '0x9999999999999999999999999999999999999999')
        self.assertEqual(qredo_transaction_info.value, '1')
        self.assertEqual(qredo_transaction_info.gasPrice, '1000')
        self.assertEqual(qredo_transaction_info.maxPriorityFeePerGas, None)
        self.assertEqual(qredo_transaction_info.maxFeePerGas, None)
        self.assertEqual(qredo_transaction_info.gasLimit, '21000')
        self.assertEqual(qredo_transaction_info.data, '')
        self.assertEqual(qredo_transaction_info.rawTX, '4YCCA-iCUgiUYkaP2Ra_J6O3bT3i5SgOUweOE-EBgICAgA')
        self.assertEqual(qredo_transaction_info.createdBy, 'EFvSMt9uGTEsDCx22sYB8BPz1bCyxAZNPKDWpJVsLKM9')
        self.assertEqual(qredo_transaction_info.network, '')
        self.assertEqual(qredo_transaction_info.chainID, '1')

    @mock.patch('requests.post', side_effect=mock_qredo_requests_post)
    def test_should_create_transaction(self, mock_post):
        """We mock the methods requests.get and requests.post via the above decorators"""
        new_transaction = QredoNewTransaction(
            from_="0x62468FD916bF27A3b76d3de2e5280e53078e13E1",
            to="0x9999999999999999999999999999999999999999",
            value="1",
            gasPrice="1000",
            maxPriorityFeePerGas=None,
            maxFeePerGas=None,
            gasLimit="21000",
            data="",
            chainID="1",
        )
        transaction = self.client.create_transaction(new_transaction)
        self.assertEqual(transaction.txID, '2ELuLA4HWIzPBQB1MSLmbOxtoB1')


if __name__ == "__main__":
    unittest.main()
