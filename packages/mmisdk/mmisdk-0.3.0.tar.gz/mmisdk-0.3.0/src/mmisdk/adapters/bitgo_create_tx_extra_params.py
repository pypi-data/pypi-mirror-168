from pydantic import BaseModel


class BitgoCreateTxExtraParams(BaseModel):
    walletId: str
