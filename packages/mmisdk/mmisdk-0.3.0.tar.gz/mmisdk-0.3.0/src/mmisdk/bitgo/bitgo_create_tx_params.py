
from typing import Optional
from pydantic import BaseModel


class BitgoCreateTxParamsInner(BaseModel):
    from_: str
    to: str
    value: str
    gasLimit: str
    gasPrice: Optional[str]
    maxPriorityFeePerGas: Optional[str]
    maxFeePerGas: Optional[str]
    data: str


class BitgoCreateTxParams(BaseModel):
    txParams: BitgoCreateTxParamsInner
