import copy
import requests
from typing import List, Union

from mmisdk.cactus.dtos import CactusCreateTxExtramParams, CactusTransaction
from mmisdk.common.transaction_params import EIP11559TxParams, LegacyTxParams
from mmisdk.utils.map_transaction_status import map_transaction_status
from mmisdk.common.custodian import Custodian
from mmisdk.common.transaction import Transaction


class Cactus(Custodian):

    def __create_access_token(self):
        """Internal method that creates an access token, necessary to authenticate other calls against Cactus Custody's API.

        Returns:
            The access token as a string.
        """
        url = f"{self.api_url}/tokens"
        payload = {"grantType": "refresh_token",
                   "refreshToken": self.refresh_token}
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

    def get_transaction(self, transaction_id, chain_id=1) -> Transaction:
        url = f"{self.api_url}/transactions"
        querystring = {"chainId": chain_id, "transactionId": transaction_id}
        payload = ""
        headers = self.__get_headers()

        response = requests.get(url, data=payload, headers=headers, params=querystring)
        response_json = response.json()

        if (len(response_json) == 0):
            raise requests.HTTPError(f"No transaction of id '{transaction_id}' on chain {chain_id}")

        # Parse and validate response
        tx = response_json[0]
        tx["from_"] = tx["from"]
        cactus_transaction = CactusTransaction(**tx)

        return self.__map_cactus_transaction_to_transaction(cactus_transaction)

    def get_transactions(self, chain_id=1) -> List[Transaction]:
        url = f"{self.api_url}/transactions"
        querystring = {"chainId": chain_id}
        payload = ""
        headers = self.__get_headers()

        response = requests.get(url, data=payload, headers=headers, params=querystring)

        # Parse and validate response
        response_json = response.json()
        response_json_parsed = list(map(inject_from_, response_json))
        cactus_transactions = list(map(lambda json: CactusTransaction(**json), response_json_parsed))

        return list(map(lambda cactus_tx: self.__map_cactus_transaction_to_transaction(cactus_tx), cactus_transactions))

    def create_transaction(self, tx_params: Union[LegacyTxParams, EIP11559TxParams], extra_params: CactusCreateTxExtramParams) -> Transaction:
        url = f"{self.api_url}/transactions"
        headers = self.__get_headers()

        # Parse and type check params
        tx_params["from_"] = tx_params["from"]
        tx_params_parsed = EIP11559TxParams(
            **tx_params) if 'type' in tx_params and tx_params['type'] == "2" else LegacyTxParams(**tx_params)
        extra_params_parsed = CactusCreateTxExtramParams(**extra_params)

        # Build the payload
        querystring = {"chainId": extra_params_parsed.chainId}
        type_ = tx_params_parsed.type  # "type" would shadow a builtin
        payload = {
            'to': tx_params_parsed.to,
            'from': tx_params_parsed.from_,
            'value': tx_params_parsed.value,
            'gasLimit': tx_params_parsed.gasLimit,
            'gasPrice': tx_params_parsed.gasPrice if type_ != "2" else None,
            'maxPriorityFeePerGas': tx_params_parsed.maxPriorityFeePerGas if type_ == "2" else None,
            'maxFeePerGas': tx_params_parsed.maxFeePerGas if type_ == "2" else None,
            'data': tx_params_parsed.data,
            'nonce': tx_params_parsed.nonce,
            'note': extra_params_parsed.note,
        }
        response = requests.post(url, json=payload, headers=headers, params=querystring)
        response_json = response.json()

        if response.status_code != 200:
            raise requests.HTTPError(
                f"Couldn't create the transaction. Request failed with status {response.status_code}: {response_json}")

        # Parse response
        response_json["from_"] = response_json["from"]
        cactus_transaction = CactusTransaction(**response_json)

        return self.__map_cactus_transaction_to_transaction(cactus_transaction)

    def __map_cactus_transaction_to_transaction(self, cactus_transaction: CactusTransaction) -> Transaction:
        return Transaction(
            id=cactus_transaction.custodian_transactionId,
            type="1" if cactus_transaction.gasPrice is not None else "2",
            from_=cactus_transaction.from_,
            to=None,
            value=None,  # TODO Why no field "value" on the response from Cactus API?
            gas=cactus_transaction.gasLimit,
            gasPrice=cactus_transaction.gasPrice,
            maxPriorityFeePerGas=cactus_transaction.maxPriorityFeePerGas,
            maxFeePerGas=cactus_transaction.maxFeePerGas,
            nonce=cactus_transaction.nonce,
            data=None,  # TODO Why no field "data" on the response from Cactus API?
            hash=cactus_transaction.transactionHash,
            status=map_transaction_status(cactus_transaction.transactionStatus, "Unknown"),
        )


def inject_from_(json):
    """This method copies the field 'from' on a json, and re-injects it under the field 'from_'. This is needed because 'from' is a reserved keyword in Python."""
    result = copy.copy(json)
    result["from_"] = result["from"]
    return result
