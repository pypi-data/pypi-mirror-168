from typing import List

import requests

from mmisdk.cactus.cactus_get_transactions_params import CactusGetTransactionsParams
from mmisdk.cactus.cactus_transaction_detail import CactusTransactionDetail
from mmisdk.cactus.cactus_tx_params import CactusTXParams
from mmisdk.common.abstract_client import AbstractClient
from mmisdk.utils.inject_from_ import inject_from_on_all


class CactusClient(AbstractClient):

    def __create_access_token(self):
        """Internal method that creates an access token, necessary to authenticate other calls against Cactus Custody's API.

        Returns:
            The access token as a string.
        """
        url = f"{self.api_url}/tokens"
        payload = {"grantType": "refresh_token",
                   "refreshToken": self.token}
        headers = {"Content-Type": "application/json"}

        response = requests.post(url,  json=payload, headers=headers)
        response_json = response.json()

        if 'jwt' not in response_json:
            raise requests.HTTPError(
                f"Couldn't create the access token, {response_json}")

        access_token = response_json["jwt"]
        return access_token

    def __get_headers(self):
        """Internal method that creates the HTTP header to use for the calls against Cactus Custody's API. It includes an authorization header that uses the access token.

        Returns:
            The HTTP header as a dictionary.
        """
        access_token = self.__create_access_token()
        return {
            "Content-Type": "application/json",
            "Authorization": 'Bearer ' + access_token
        }

    def get_transactions(self, params: CactusGetTransactionsParams) -> List[CactusTransactionDetail]:
        url = f"{self.api_url}/transactions"
        querystring = params.dict()
        querystring["from"] = querystring["from_"]
        payload = ""
        headers = self.__get_headers()

        response = requests.get(url, data=payload, headers=headers, params=querystring)

        # Parse and validate response
        response_json = response.json()
        response_json_parsed = inject_from_on_all(response_json)
        return list(map(lambda json: CactusTransactionDetail(**json), response_json_parsed))

    def create_transaction(self, chain_id: str, params: CactusTXParams) -> CactusTransactionDetail:
        url = f"{self.api_url}/transactions"
        headers = self.__get_headers()
        querystring = {"chainId": chain_id}
        payload = params.dict()
        payload["from"] = payload["from_"]
        response = requests.post(url, json=payload, headers=headers, params=querystring)
        response_json = response.json()

        if response.status_code != 200:
            raise requests.HTTPError(
                f"Couldn't create the transaction. Request failed with status {response.status_code}: {response_json}")

        # Parse response
        response_json["from_"] = response_json["from"]
        return CactusTransactionDetail(**response_json)
