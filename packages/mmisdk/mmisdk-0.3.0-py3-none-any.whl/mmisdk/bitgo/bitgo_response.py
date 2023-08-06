from typing import Generic, TypeVar

from pydantic.generics import GenericModel

from mmisdk.bitgo.bitgo_response_meta import BitgoResponseMeta


T = TypeVar("T")


class BitgoResponse(GenericModel, Generic[T]):
    data: T
    _meta: BitgoResponseMeta
