import logging
from typing import Union

from mmisdk.adapters.bitgo_create_tx_extra_params import BitgoCreateTxExtraParams

from mmisdk.bitgo.bitgo_client import BitgoClient
from mmisdk.bitgo.bitgo_create_tx_params import BitgoCreateTxParams
from mmisdk.bitgo.bitgo_transaction import BitgoTransaction
from mmisdk.common.custodian import Custodian
from mmisdk.common.transaction import Transaction
from mmisdk.common.transaction_params import EIP1559TxParams, LegacyTxParams
from mmisdk.utils.map_transaction_status import map_transaction_status


class BitgoAdapter(Custodian):

    def __init__(self, client: BitgoClient) -> None:
        self.client = client

    def get_transaction(self, transaction_id, chain_id=1) -> Transaction:
        bitgo_list_response = self.client.get_transaction_by_custodian_tx_id(transaction_id)
        bitgo_transaction = bitgo_list_response.data[0]
        return self.__map_bitgo_transaction_to_transaction(bitgo_transaction)

    def create_transaction(self, tx_params: Union[LegacyTxParams, EIP1559TxParams], extra_params) -> Transaction:
        # Parse and type check params
        type_ = tx_params["type"] if 'type' in tx_params else 1
        tx_params_parsed = EIP1559TxParams(**tx_params) if type_ == 2 else LegacyTxParams(**tx_params)
        extra_params_parsed = BitgoCreateTxExtraParams(**extra_params)

        gasPrice = tx_params_parsed.gasPrice if type_ == 1 else None
        maxPriorityFeePerGas = tx_params_parsed.maxPriorityFeePerGas if type_ == 2 else None
        maxFeePerGas = tx_params_parsed.maxFeePerGas if type_ == 2 else None

        bitgo_create_tx_params = BitgoCreateTxParams(txParams={
            "from_": tx_params_parsed.from_,
            "to": tx_params_parsed.to,
            "value": tx_params_parsed.value,
            "gasLimit": tx_params_parsed.gas,
            "gasPrice": gasPrice,
            "maxPriorityFeePerGas": maxPriorityFeePerGas,
            "maxFeePerGas": maxFeePerGas,
            "data": tx_params_parsed.data
        })

        bitgo_response = self.client.create_transaction(extra_params_parsed.walletId, bitgo_create_tx_params)
        bitgo_transaction = bitgo_response.data
        return self.__map_bitgo_transaction_to_transaction(bitgo_transaction)

    def __map_bitgo_transaction_to_transaction(self, bitgo_transaction: BitgoTransaction) -> Transaction:
        logging.warning(
            "Can't derive the transaction's type, because the BitGo's API returns incomplete data. Using type = '1' by default, but it might be wrong.")
        return Transaction(
            id=bitgo_transaction.custodianTransactionId,
            type="1",  # TODO We can't derive this since no field gasPrice/maxPriorityFeePerGas/maxFeePerGas on data returned by Bitgo's API
            from_=bitgo_transaction.from_,
            to=bitgo_transaction.to,
            value=bitgo_transaction.value,
            gas=bitgo_transaction.gasLimit,
            gasPrice=None,
            maxPriorityFeePerGas=None,
            maxFeePerGas=None,
            nonce=None,
            data=bitgo_transaction.data,
            hash=bitgo_transaction.transactionHash,
            status=map_transaction_status(bitgo_transaction.transactionStatus, "Unknown"),
        )
