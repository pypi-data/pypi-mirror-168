

from pydantic import BaseModel


class BitgoResponseMeta(BaseModel):
    reqId: str
