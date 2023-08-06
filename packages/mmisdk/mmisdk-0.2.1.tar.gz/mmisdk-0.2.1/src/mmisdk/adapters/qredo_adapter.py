from typing import List

import requests

from mmisdk.adapters.qredo_create_tx_extra_params import QredoCreateTxExtraParams
from mmisdk.common.custodian import Custodian
from mmisdk.common.transaction import Transaction
from mmisdk.common.transaction_params import EIP1559TxParams
from mmisdk.common.transaction_params import LegacyTxParams
from mmisdk.qredo.qredo_client import QredoClient
from mmisdk.qredo.qredo_new_transaction import QredoNewTransaction
from mmisdk.qredo.qredo_transaction_info import QredoTransactionInfo
from mmisdk.utils.map_transaction_status import map_transaction_status


class QredoAdapter(Custodian):

    def __init__(self, client: QredoClient) -> None:
        self.client = client

    def get_transaction(self, transaction_id: str, chain_id=1) -> Transaction:
        qredo_transaction_info = self.client.get_transaction(transaction_id)
        return self.__map_qredo_transaction_info_to_transaction(qredo_transaction_info)

    def get_transactions(self, chain_id=1) -> List[Transaction]:
        raise requests.HTTPError("Not implemented")

    def create_transaction(self, tx_params, extra_params) -> Transaction:
        # Parse and type check params
        type_ = tx_params["type"] if 'type' in tx_params else 1
        tx_params_parsed = EIP1559TxParams(**tx_params) if type_ == 2 else LegacyTxParams(**tx_params)
        extra_params_parsed = QredoCreateTxExtraParams(**extra_params)

        gas_limit = tx_params_parsed.gas if type_ == 1 else None
        max_priority_fee_per_gas = tx_params_parsed.maxPriorityFeePerGas if type_ == 2 else None
        max_fee_per_gas = tx_params_parsed.maxFeePerGas if type_ == 2 else None

        new_transaction = QredoNewTransaction(
            from_=tx_params_parsed.from_,
            to=tx_params_parsed.to,
            value=tx_params_parsed.value,
            gasPrice=tx_params_parsed.gasPrice,
            maxPriorityFeePerGas=max_priority_fee_per_gas,
            maxFeePerGas=max_fee_per_gas,
            gasLimit=gas_limit,
            data=tx_params_parsed.data or "",
            chainID=extra_params_parsed.chainID
        )
        qredo_transaction_info = self.client.create_transaction(new_transaction)
        return self.__map_qredo_transaction_info_to_transaction(qredo_transaction_info)

    def __map_qredo_transaction_info_to_transaction(self, qredo_transaction_info: QredoTransactionInfo) -> Transaction:
        return Transaction(
            id=qredo_transaction_info.txID,
            type="1" if qredo_transaction_info.gasPrice is not None else "2",
            from_=qredo_transaction_info.from_,
            to=qredo_transaction_info.to,
            value=qredo_transaction_info.value,
            gas=qredo_transaction_info.gasLimit,
            gasPrice=qredo_transaction_info.gasPrice,
            maxPriorityFeePerGas=None,
            maxFeePerGas=None,
            nonce=qredo_transaction_info.nonce,
            data=qredo_transaction_info.data,
            hash=qredo_transaction_info.txHash,
            status=map_transaction_status(qredo_transaction_info.status, "Unknown"),
        )
