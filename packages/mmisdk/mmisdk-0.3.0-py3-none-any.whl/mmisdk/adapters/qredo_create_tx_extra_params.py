from pydantic import BaseModel


class QredoCreateTxExtraParams(BaseModel):
    chainID: str
