from mmisdk.mocks.mock_bitgo_create_tx_response import MOCK_BITGO_CREATE_TX_RESPONSE
from mmisdk.mocks.mock_response import MockResponse


def mock_bitgo_requests_post(*args, **kwargs):

    # Mock the request that creates a transaction
    if args[0].__contains__('/tx/build'):
        return MockResponse(MOCK_BITGO_CREATE_TX_RESPONSE, 201)

    return MockResponse(None, 404)
