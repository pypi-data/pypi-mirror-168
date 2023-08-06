from typing import Optional

from pydantic import BaseModel


class CactusTXParams(BaseModel):
    """ Refer to ./custody-defi-api-4.yaml for more details """
    from_: str
    to: str
    gasLimit: str
    value: str
    data: Optional[str]  # In practice it is indeed optional, contrary to what custody-defi-api-4.yaml says
    gasPrice: Optional[str]
    maxFeePerGas: Optional[str]
    maxPriorityFeePerGas: Optional[str]
