from mmisdk.mocks.mock_qredo_transaction_info import MOCK_QREDO_TRANSACTION_INFO
from mmisdk.mocks.mock_response import MockResponse


def mock_qredo_requests_get(*args, **kwargs):
    """ This method will be used by the mock to replace requests.get"""

    # Mock the request that gets the transaction
    if args[0].__contains__('/connect/transaction'):
        return MockResponse(MOCK_QREDO_TRANSACTION_INFO, 200)

    return MockResponse(None, 404)
