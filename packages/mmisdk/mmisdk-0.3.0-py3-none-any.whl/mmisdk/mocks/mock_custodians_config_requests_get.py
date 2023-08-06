from mmisdk.mocks.mock_custodians_config import MOCK_CUSTODIANS_CONFIG
from mmisdk.mocks.mock_response import MockResponse


def mock_custodians_config_requests_get(*args, **kwargs):
    """ This method will be used by the mock to replace requests.get"""

    # Mock the request that gets the custodian configs
    if args[0].__contains__('/configuration/default'):
        return MockResponse(MOCK_CUSTODIANS_CONFIG, 200)

    return MockResponse(None, 404)
