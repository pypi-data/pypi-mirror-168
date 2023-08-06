from typing import Optional
from pydantic import BaseModel

""""
DTOs and types specific to Cactus Custodian.
Check the file ./custody-defi-api-4.yaml for a complete reference.
"""


class CactusCreateTxExtramParams(BaseModel):
    chainId: str
    note: Optional[str]


class CactusTransaction(BaseModel):
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
