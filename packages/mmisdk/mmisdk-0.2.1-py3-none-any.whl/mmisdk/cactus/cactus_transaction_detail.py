from typing import Optional

from pydantic import BaseModel


class CactusTransactionDetail(BaseModel):
    """ Refer to ./custody-defi-api-4.yaml for more details """
    transactionStatus: str
    transactionHash: Optional[str]
    custodian_transactionId: Optional[str]
    gasPrice: Optional[str]
    maxFeePerGas: Optional[str]
    maxPriorityFeePerGas: Optional[str]
    gasLimit: Optional[str]
    nonce: Optional[str]
    from_: Optional[str]
    signature: Optional[str]
