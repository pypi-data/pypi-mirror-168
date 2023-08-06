from mmisdk.mocks.mock_cactus_transaction_detail_1 import MOCK_CACTUS_TRANSACTION_DETAIL_1
from mmisdk.mocks.mock_response import MockResponse


def mock_cactus_requests_post(*args, **kwargs):
    """ This method will be used by the mock to replace requests.post"""

    # Mock the request that creates the access token
    if args[0].__contains__('/tokens'):
        return MockResponse({"jwt": "some-access-token"}, 200)

    # Mock the request that creates a transaction
    if args[0].__contains__('/transactions'):
        return MockResponse(MOCK_CACTUS_TRANSACTION_DETAIL_1, 200)

    return MockResponse(None, 404)
