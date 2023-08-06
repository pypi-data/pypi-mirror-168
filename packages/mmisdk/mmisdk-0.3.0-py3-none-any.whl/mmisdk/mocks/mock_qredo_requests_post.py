from mmisdk.mocks.mock_qredo_transaction_info import MOCK_QREDO_TRANSACTION_INFO
from mmisdk.mocks.mock_response import MockResponse


def mock_qredo_requests_post(*args, **kwargs):
    """ This method will be used by the mock to replace requests.post"""

    # Mock the request that creates the access token
    if args[0].__contains__('/connect/token'):
        return MockResponse({"access_token": "some-access-token"}, 200)

    # Mock the request that creates a transaction
    if args[0].__contains__('/connect/transaction'):
        return MockResponse(MOCK_QREDO_TRANSACTION_INFO, 200)

    return MockResponse(None, 404)
