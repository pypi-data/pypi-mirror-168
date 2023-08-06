from typing import Optional

from pydantic import BaseModel


class CactusGetTransactionsParams(BaseModel):
    """ Refer to ./custody-defi-api-4.yaml for more details """
    chainId: str
    from_: Optional[str]
    transactionId: Optional[str]
    transactionHash: Optional[str]
