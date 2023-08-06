from mmisdk.mocks.mock_bitgo_get_tx_by_custodian_id import MOCK_BITGO_GET_TX_BY_CUSTODIAN_ID
from mmisdk.mocks.mock_response import MockResponse


def mock_bitgo_requests_get(*args, **kwargs):
    """ This method will be used by the mock to replace requests.get"""

    if args[0].__contains__('INVALID-CUSTODIAN-TX-ID'):
        return MockResponse({
            "error": "Did not find match for tx id: INVALID-CUSTODIAN-TX-ID",
            "errorName": "Error",
            "reqId": "unk-rktoh37uhl63sm8i1vfe",
            "context": {
                "_meta": {
                    "reqId": "unk-rktoh37uhl63sm8i1vfe"
                }
            }
        }, 404)

    if args[0].__contains__('/eth/wallets/transactions/'):
        return MockResponse(MOCK_BITGO_GET_TX_BY_CUSTODIAN_ID, 200)

    return MockResponse(None, 404)
