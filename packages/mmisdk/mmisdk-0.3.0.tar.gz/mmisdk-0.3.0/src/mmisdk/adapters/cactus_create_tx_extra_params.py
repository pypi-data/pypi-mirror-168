from typing import Optional

from pydantic import BaseModel


class CactusCreateTxExtraParams(BaseModel):
    chainId: str
    note: Optional[str]
