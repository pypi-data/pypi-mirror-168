from enum import Enum
from typing import Dict
from typing import List
from typing import Optional

from pydantic import BaseModel


class QredoTransactionEvent(BaseModel):
    id: str
    timestamp: int
    status: str
    message: str


class QredoTransactionStatus(str, Enum):
    PENDING = "pending"
    CREATED = "created"
    AUTHORIZED = "authorized"
    APPROVED = "approved"
    EXPIRED = "expired"
    CANCELLED = "cancelled"
    REJECTED = "rejected"
    SIGNED = "signed"
    SCHEDULED = "scheduled"
    PUSHED = "pushed"
    CONFIRMED = "confirmed"
    MINED = "mined"
    FAILED = "failed"


class QredoTransactionInfo(BaseModel):
    txID: str
    txHash: str
    status: QredoTransactionStatus
    nonce: int
    from_: str
    to: str
    value: str
    gasPrice: Optional[str]
    maxPriorityFeePerGas: Optional[str]
    gasLimit: str
    maxFeePerGas: Optional[str]
    data: str
    rawTX: str
    createdBy: str
    network: str
    chainID: str
    timestamps: Dict
    events: List[QredoTransactionEvent]
