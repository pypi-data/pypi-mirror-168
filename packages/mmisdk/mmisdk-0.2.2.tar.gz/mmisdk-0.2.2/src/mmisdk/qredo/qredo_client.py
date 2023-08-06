import requests

from mmisdk.common.abstract_client import AbstractClient
from mmisdk.qredo.qredo_new_transaction import QredoNewTransaction
from mmisdk.qredo.qredo_transaction_info import QredoTransactionInfo


class QredoClient(AbstractClient):

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

    def get_transaction(self, tx_id: str) -> QredoTransactionInfo:
        url = self.api_url + '/connect/transaction/' + tx_id
        payload = ""
        headers = self.__get_headers()

        response = requests.get(url, data=payload, headers=headers)
        if (response.status_code != 200):
            raise requests.HTTPError(
                f"Couldn't get the transaction, {response.text}")

        # Parse response
        response_json = response.json()
        response_json["from_"] = response.json()["from"]

        return QredoTransactionInfo(**response_json)

    def create_transaction(self, new_transaction: QredoNewTransaction) -> QredoTransactionInfo:
        url = self.api_url + "/connect/transaction"
        headers = self.__get_headers()

        payload = new_transaction.dict()
        payload["from"] = payload["from_"]
        response = requests.post(url, json=payload, headers=headers)

        if (response.status_code != 200):
            raise requests.HTTPError(
                f"Couldn't create the transaction, {response.text}")

        # Parse response
        response_json = response.json()
        response_json["from_"] = response.json()["from"]
        return QredoTransactionInfo(**response_json)
