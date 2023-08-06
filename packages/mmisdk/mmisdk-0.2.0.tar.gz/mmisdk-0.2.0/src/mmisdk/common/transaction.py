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
    """Common data format returned by all custodian clients."""
    id: str
    type: str
    from_: str
    to: Optional[str]
    value: Optional[str]
    gas: str
    gasPrice: Optional[str]
    maxPriorityFeePerGas: Optional[str]
    maxFeePerGas: Optional[str]
    nonce: Optional[str]
    data: Optional[str]
    hash: Optional[str]
    status: TransactionStatus
