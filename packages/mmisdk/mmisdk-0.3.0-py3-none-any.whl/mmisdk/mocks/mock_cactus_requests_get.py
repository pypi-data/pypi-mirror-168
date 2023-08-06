from mmisdk.mocks.mock_cactus_transaction_detail_0 import MOCK_CACTUS_TRANSACTION_DETAIL_0
from mmisdk.mocks.mock_cactus_transaction_detail_1 import MOCK_CACTUS_TRANSACTION_DETAIL_1
from mmisdk.mocks.mock_response import MockResponse


def mock_cactus_requests_get(*args, **kwargs):
    """ This method will be used by the mock to replace requests.get"""
    # Mock the request that gets all transactions
    if args[0].__contains__('/transactions'):
        return MockResponse([MOCK_CACTUS_TRANSACTION_DETAIL_0, MOCK_CACTUS_TRANSACTION_DETAIL_1], 200)

    return MockResponse(None, 404)
