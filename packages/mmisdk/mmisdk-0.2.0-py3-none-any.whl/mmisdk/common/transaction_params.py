from typing import Optional

from pydantic import BaseModel


class BaseTxParams(BaseModel):
    from_: str   # In Python, "from" is a reserved keyword
    to: str
    value: Optional[str]
    data: Optional[str]
    gasLimit: str
    gas: Optional[str]
    nonce: Optional[str]


class LegacyTxParams(BaseTxParams):
    type = 1
    gasPrice: str


class EIP11559TxParams(BaseTxParams):
    type = 2
    maxPriorityFeePerGas: str
    maxFeePerGas: str
