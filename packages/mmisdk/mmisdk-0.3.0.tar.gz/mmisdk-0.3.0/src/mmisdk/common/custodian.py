from abc import abstractmethod
from typing import List
from typing import Union

from mmisdk.common.abstract_client import AbstractClient
from mmisdk.common.transaction import Transaction
from mmisdk.common.transaction_params import EIP1559TxParams
from mmisdk.common.transaction_params import LegacyTxParams


class Custodian(AbstractClient):
    @abstractmethod
    def get_transaction(self, transaction_id, chain_id=1) -> Transaction:
        """Gets the transaction of passed id, on passed chain id, that was submitted to the custodian.

         Args:
             transaction_id: The custodian-specific transaction id as a string.
             chain_id: (Optional) The id of the chain where the transaction happens. Default is 1.

         Returns:
             The transaction of passed id.
         """
        raise NotImplementedError()

    @abstractmethod
    def get_transactions(self, chain_id=1) -> List[Transaction]:
        """Gets all transactions on passed chain id that were submitted to the custodian. Scope might be limited to the scope of your refresh token.

        Args:
            chain_id: (Optional) The id of the chain where the transaction happens. Default is 1.

        Returns:
            The transaction of passed id.
        """
        raise NotImplementedError()

    @abstractmethod
    def create_transaction(self, tx_params: Union[LegacyTxParams, EIP1559TxParams], extra_params) -> Transaction:
        """
        Creates a transaction from the passed parameters a submits it to the custodian's API.

        Args:
            tx_params: The params to create the transaction with. Must map to either a LegacyTxParams or EIP1559TxParams.
            extra_params: Custodian-specific extra parameters. Refer to the types[custodian]_create_tx_extra_params.py for specific values.
        """
        raise NotImplementedError()
