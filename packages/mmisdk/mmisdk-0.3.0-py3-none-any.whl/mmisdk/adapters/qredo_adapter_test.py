import unittest
from unittest import mock


from mmisdk.adapters.qredo_adapter import QredoAdapter
from mmisdk.mocks.mock_legacy_tx_params import MOCK_LEGACY_TX_PARAMS
from mmisdk.mocks.mock_qredo_requests_get import mock_qredo_requests_get
from mmisdk.mocks.mock_qredo_requests_post import mock_qredo_requests_post
from mmisdk.qredo.qredo_client import QredoClient


class QredoAdapterTest(unittest.TestCase):
    """Test Class"""
    @classmethod
    def setUpClass(cls):
        client = QredoClient("http://some-url", "some-refresh-token")
        cls.custodian = QredoAdapter(client)

    def test_should_be_defined(self):
        self.assertIsNotNone(self.custodian)

    def test_should_get_transactions(self):
        with self.assertRaises(NotImplementedError):
            self.custodian.get_transactions(1)

    @mock.patch('requests.get', side_effect=mock_qredo_requests_get)
    @mock.patch('requests.post', side_effect=mock_qredo_requests_post)
    def test_should_get_transaction(self, mock_get, mock_post):
        transaction = self.custodian.get_transaction("2ELuLA4HWIzPBQB1MSLmbOxtoB1")
        self.assertEqual(transaction.id, '2ELuLA4HWIzPBQB1MSLmbOxtoB1')
        self.assertEqual(transaction.type, '1')
        self.assertEqual(transaction.status.finished, False)
        self.assertEqual(transaction.status.submitted, False)
        self.assertEqual(transaction.status.signed, False)
        self.assertEqual(transaction.status.success, False)
        self.assertEqual(transaction.status.displayText, "Authorized")
        self.assertEqual(transaction.status.reason, "Unknown")

    @mock.patch('requests.post', side_effect=mock_qredo_requests_post)
    def test_should_create_transaction(self, mock_post):
        extra_params = {
            "chainID": "1",
        }
        transaction = self.custodian.create_transaction(MOCK_LEGACY_TX_PARAMS, extra_params)
        self.assertEqual(transaction.id, '2ELuLA4HWIzPBQB1MSLmbOxtoB1')


if __name__ == "__main__":
    unittest.main()
