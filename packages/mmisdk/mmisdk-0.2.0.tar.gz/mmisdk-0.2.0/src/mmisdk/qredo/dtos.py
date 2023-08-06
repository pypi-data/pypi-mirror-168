from typing import Dict, List, Optional
from pydantic import BaseModel

""""
DTOs and types specific to Qredo.
"""


class QredoCreateTxExtramParams(BaseModel):
    chainId: str
    note: Optional[str]


class QredoTransactionEvent(BaseModel):
    id: str
    timestamp: int
    status: str
    message: str


class QredoTransaction(BaseModel):
    txID: str
    txHash: str
    status: str
    timestamps: Dict
    events: List[QredoTransactionEvent]
    nonce: int
    gasLimit: str
    gasPrice: Optional[str]
    maxFeePerGas: Optional[str]
    maxPriorityFeePerGas: Optional[str]
    from_: str
    to: str
    value: str
    data: str
    rawTX: str
    createdBy: str
    accountID: str
    network: str
    chainID: str
