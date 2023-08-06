from abc import abstractmethod
from typing import List, Union

from mmisdk.common.transaction import Transaction
from mmisdk.common.transaction_params import EIP11559TxParams, LegacyTxParams


class Custodian:
    """Generic class that each custodian client inherits from."""

    def __init__(self, api_url, refresh_token):
        self.api_url = api_url
        self.refresh_token = refresh_token

    @abstractmethod
    def get_transaction(self, transaction_id) -> Transaction:
        """Gets the transaction of passed id, on passed chain id, that was submitted to the custodian.

         Args:
             transaction_id: The custodian-specific transaction id as a string.
             chain_id: (Optional) The id of the chain where the transaction happens. Default is 1.

         Returns:
             The transaction of passed id.
         """
        pass

    @abstractmethod
    def get_transactions(self, chain_id) -> List[Transaction]:
        """Gets all transactions on passed chain id that were submitted to the custodian. Scope might be limited to the scope of your refresh token.

        Args:
            chain_id: (Optional) The id of the chain where the transaction happens. Default is 1.

        Returns:
            The transaction of passed id.
        """
        pass

    @abstractmethod
    def create_transaction(self, tx_params: Union[LegacyTxParams, EIP11559TxParams], extra_params) -> Transaction:
        """
        Creates a transaction from the passed parameters a submits it to the custodian's API.

        Args:
            tx_params: The params to create the transaction with. Either LegacyTxParams or EIP11559TxParams.
            extra_params: Custodian-specific extra parameters. Refer to the types mmisdk.[custodian].dtos.CreateTxExtramParams defined in each custodian module for supported values.
        """
        pass
