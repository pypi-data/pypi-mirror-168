from typing import Dict, Optional

from pydantic import BaseModel

# Using "Optional" on all fields as we're missing specific API docs for BitGo


class BitgoTransaction(BaseModel):
    transactionStatus: Optional[str]
    custodianTransactionId: Optional[str]
    from_: Optional[str]
    to: Optional[str]
    coin: Optional[str]
    value: Optional[str]
    gasLimit: Optional[str]
    userId: Optional[str]
    createdTime: Optional[str]
    data: Optional[str]
    decodedData: Optional[Dict]
    transactionHash: Optional[str]
