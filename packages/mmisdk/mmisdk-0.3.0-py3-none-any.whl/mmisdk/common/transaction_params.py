from typing import Optional

from pydantic import BaseModel


class BaseTxParams(BaseModel):
    from_: str   # In Python, "from" is a reserved keyword
    to: str
    value: Optional[str]
    data: Optional[str]
    gas: Optional[str]  # Same as gasLimit
    nonce: Optional[str]


class LegacyTxParams(BaseTxParams):
    type = 1
    gasPrice: str


class EIP1559TxParams(BaseTxParams):
    type = 2
    maxPriorityFeePerGas: str
    maxFeePerGas: str
