from typing import Optional

from pydantic import BaseModel


class QredoNewTransaction(BaseModel):
    from_: str
    to: str
    value: str
    gasPrice: Optional[str]
    maxPriorityFeePerGas:  Optional[str]
    maxFeePerGas:  Optional[str]
    gasLimit: str
    data: str
    chainID: str
