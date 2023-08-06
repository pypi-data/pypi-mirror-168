from typing import Optional

from pydantic import BaseModel


class TransactionStatus(BaseModel):
    finished: bool
    submitted: bool
    signed: bool
    success: bool
    displayText: str
    reason: str


class Transaction(BaseModel):
    id: str
    type: str
    from_: str
    to: Optional[str]
    value: Optional[str]  # In Wei
    gas: str  # Same as gasLimit
    gasPrice: Optional[str]
    maxPriorityFeePerGas: Optional[str]
    maxFeePerGas: Optional[str]
    nonce: Optional[str]
    data: Optional[str]
    hash: Optional[str]
    status: TransactionStatus
