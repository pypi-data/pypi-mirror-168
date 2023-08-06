from __future__ import annotations

import typing
from uuid import UUID
from pydantic.json import ENCODERS_BY_TYPE

if typing.TYPE_CHECKING:
    from pydantic.typing import CallableGenerator


avro_schema: typing.Final[
    str
] = '{"type": "fixed", "namespace": "Energistics.Etp.v12.Datatypes", "name": "Uuid", "size": 16, "fullName": "Energistics.Etp.v12.Datatypes.Uuid", "depends": []}'


class Uuid(bytes):

    size: typing.Final[int] = 16

    @classmethod
    def __get_validators__(cls) -> CallableGenerator:
        yield cls.validate

    @classmethod
    def validate(cls, value: typing.Any) -> Uuid:

        if isinstance(value, cls):
            return value

        x: bytes

        if isinstance(value, UUID):
            x = value.bytes
        elif isinstance(value, str):
            x = UUID(hex=value).bytes
        elif isinstance(value, (bytes, bytearray)):
            x = value
        else:
            raise ValueError("Value must be either UUID, str or bytes")

        if len(x) != cls.size:
            raise ValueError(f"invalid format, actual size != from {cls.size}")

        return cls(x)

    def __str__(self) -> str:
        return self.to_str()

    def to_str(self) -> str:
        return str(UUID(bytes=self))


ENCODERS_BY_TYPE[Uuid] = lambda v: v.to_str()
