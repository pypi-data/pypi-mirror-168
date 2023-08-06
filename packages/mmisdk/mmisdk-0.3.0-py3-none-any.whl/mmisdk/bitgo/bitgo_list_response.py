from typing import Generic, List, TypeVar
from pydantic.generics import GenericModel

from mmisdk.bitgo.bitgo_response_meta import BitgoResponseMeta


T = TypeVar("T")


class BitgoListResponse(GenericModel, Generic[T]):
    data: List[T]
    meta: BitgoResponseMeta
