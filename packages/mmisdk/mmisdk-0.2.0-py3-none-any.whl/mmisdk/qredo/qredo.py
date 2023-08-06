import requests
from typing import List, Union
from mmisdk.common.custodian import Custodian
from mmisdk.common.transaction import Transaction
from mmisdk.common.transaction_params import EIP11559TxParams
from mmisdk.common.transaction_params import LegacyTxParams
from mmisdk.qredo.dtos import QredoCreateTxExtramParams, QredoTransaction
from mmisdk.utils.map_transaction_status import map_transaction_status


class Qredo(Custodian):

    def __create_access_token(self):
        """Internal method that creates an access token, necessary to authenticate other calls against Qredo's API.

        Returns:
            The access token as a string.
        """
        url = self.api_url+'/connect/token'
        querystring = {"grant_type": "refresh_token",
                       "refresh_token": self.refresh_token}
        payload = ""

        response = requests.post(url, data=payload, params=querystring)
        if (response.status_code != 200):
            raise requests.HTTPError(
                f"Couldn't create the access token, {response.text}")

        access_token = response.json()["access_token"]
        return access_token

    def __get_headers(self):
        """Returns the HTTP header to use in requests to the custodian"""
        access_token = self.__create_access_token()
        return {
            "Content-Type": "application/json",
            "Authorization": 'Bearer ' + access_token
        }

    def get_transaction(self, transaction_id, chain_id=1) -> Transaction:
        url = self.api_url + '/connect/transaction/' + transaction_id
        payload = ""
        headers = self.__get_headers()

        response = requests.get(url, data=payload, headers=headers)
        if (response.status_code != 200):
            raise requests.HTTPError(
                f"Couldn't get the transaction, {response.text}")

        # Parse response
        response_json = response.json()
        response_json["from_"] = response.json()["from"]
        qredo_transaction = QredoTransaction(**response_json)

        return self.__map_qredo_transaction_to_transaction(qredo_transaction)

    def get_transactions(self, chain_id=1) -> List[Transaction]:
        raise requests.HTTPError("Not implemented")

    def create_transaction(self, tx_params: Union[LegacyTxParams, EIP11559TxParams], extra_params: QredoCreateTxExtramParams) -> Transaction:
        url = self.api_url + "/connect/transaction"
        headers = self.__get_headers()

        # Parse and type check params
        qredo_tx_details_parsed = QredoCreateTxExtramParams(**extra_params)
        tx_params["from_"] = tx_params["from"]
        tx_params_parsed = EIP11559TxParams(
            **tx_params) if 'type' in tx_params and tx_params['type'] == "2" else LegacyTxParams(**tx_params)

        # Build the payload
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
            'chainId': qredo_tx_details_parsed.chainId,
            'note': qredo_tx_details_parsed.note,
        }

        response = requests.post(url, json=payload, headers=headers)

        if (response.status_code != 200):
            raise requests.HTTPError(
                f"Couldn't create the transaction, {response.text}")

        # Parse response
        response_json = response.json()
        response_json["from_"] = response.json()["from"]
        qredo_transaction = QredoTransaction(**response_json)

        return self.__map_qredo_transaction_to_transaction(qredo_transaction)

    def __map_qredo_transaction_to_transaction(self, qredo_transaction: QredoTransaction) -> Transaction:
        return Transaction(
            id=qredo_transaction.txID,
            type="1" if qredo_transaction.gasPrice is not None else "2",
            from_=qredo_transaction.from_,
            to=qredo_transaction.to,
            value=qredo_transaction.value,
            gas=qredo_transaction.gasLimit,
            gasPrice=qredo_transaction.gasPrice,
            maxPriorityFeePerGas=None,
            maxFeePerGas=None,
            nonce=qredo_transaction.nonce,
            data=qredo_transaction.data,
            hash=qredo_transaction.txHash,
            status=map_transaction_status(qredo_transaction.status, "Unknown"),
        )
