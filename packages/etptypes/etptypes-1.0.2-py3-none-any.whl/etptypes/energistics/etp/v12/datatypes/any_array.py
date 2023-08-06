# -*- coding: utf-8 -*-

""" avro python class for file: any_array """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


from etptypes.energistics.etp.v12.datatypes.array_of_boolean import ArrayOfBoolean

from etptypes.energistics.etp.v12.datatypes.array_of_int import ArrayOfInt

from etptypes.energistics.etp.v12.datatypes.array_of_long import ArrayOfLong

from etptypes.energistics.etp.v12.datatypes.array_of_float import ArrayOfFloat

from etptypes.energistics.etp.v12.datatypes.array_of_double import ArrayOfDouble

from etptypes.energistics.etp.v12.datatypes.array_of_string import ArrayOfString


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "AnyArray", "fields": [{"name": "item", "type": [{"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "ArrayOfBoolean", "fields": [{"name": "values", "type": {"type": "array", "items": "boolean"}}], "fullName": "Energistics.Etp.v12.Datatypes.ArrayOfBoolean", "depends": []}, {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "ArrayOfInt", "fields": [{"name": "values", "type": {"type": "array", "items": "int"}}], "fullName": "Energistics.Etp.v12.Datatypes.ArrayOfInt", "depends": []}, {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "ArrayOfLong", "fields": [{"name": "values", "type": {"type": "array", "items": "long"}}], "fullName": "Energistics.Etp.v12.Datatypes.ArrayOfLong", "depends": []}, {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "ArrayOfFloat", "fields": [{"name": "values", "type": {"type": "array", "items": "float"}}], "fullName": "Energistics.Etp.v12.Datatypes.ArrayOfFloat", "depends": []}, {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "ArrayOfDouble", "fields": [{"name": "values", "type": {"type": "array", "items": "double"}}], "fullName": "Energistics.Etp.v12.Datatypes.ArrayOfDouble", "depends": []}, {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "ArrayOfString", "fields": [{"name": "values", "type": {"type": "array", "items": "string"}}], "fullName": "Energistics.Etp.v12.Datatypes.ArrayOfString", "depends": []}, "bytes"]}], "fullName": "Energistics.Etp.v12.Datatypes.AnyArray", "depends": ["Energistics.Etp.v12.Datatypes.ArrayOfBoolean", "Energistics.Etp.v12.Datatypes.ArrayOfInt", "Energistics.Etp.v12.Datatypes.ArrayOfLong", "Energistics.Etp.v12.Datatypes.ArrayOfFloat", "Energistics.Etp.v12.Datatypes.ArrayOfDouble", "Energistics.Etp.v12.Datatypes.ArrayOfString"]}'


class AnyArray(ETPModel):

    item: typing.Union[
        ArrayOfBoolean,
        ArrayOfInt,
        ArrayOfLong,
        ArrayOfFloat,
        ArrayOfDouble,
        ArrayOfString,
        Strict[bytes],
    ] = Field(alias="item")

    def dict(self, *args, **kwargs) -> dict[str, object]:
        if isinstance(self.item, ArrayOfFloat):
            return {
                "item": (
                    "Energistics.Etp.v12.Datatypes.ArrayOfFloat",
                    {"values": self.item.values},
                )
            }
        elif isinstance(self.item, ArrayOfDouble):
            return {
                "item": (
                    "Energistics.Etp.v12.Datatypes.ArrayOfDouble",
                    {"values": self.item.values},
                )
            }
        elif isinstance(self.item, ArrayOfInt):
            return {
                "item": (
                    "Energistics.Etp.v12.Datatypes.ArrayOfInt",
                    {"values": self.item.values},
                )
            }
        elif isinstance(self.item, ArrayOfLong):
            return {
                "item": (
                    "Energistics.Etp.v12.Datatypes.ArrayOfLong",
                    {"values": self.item.values},
                )
            }
        elif isinstance(self.item, ArrayOfBoolean):
            return {
                "item": (
                    "Energistics.Etp.v12.Datatypes.ArrayOfBoolean",
                    {"values": self.item.values},
                )
            }
        elif isinstance(self.item, ArrayOfString):
            return {
                "item": (
                    "Energistics.Etp.v12.Datatypes.ArrayOfString",
                    {"values": self.item.values},
                )
            }
        else:
            return super().dict(*args, **kwargs)

    @validator("item", pre=True, always=True)
    def validate_item_type(cls, v):
        if isinstance(v, (tuple, list)):
            if v[0].endswith("ArrayOfBoolean"):
                return ArrayOfBoolean.construct(values=v[1]["values"])
            elif v[0].endswith("ArrayOfInt"):
                return ArrayOfInt.construct(values=v[1]["values"])
            elif v[0].endswith("ArrayOfLong"):
                return ArrayOfLong.construct(values=v[1]["values"])
            elif v[0].endswith("ArrayOfFloat"):
                return ArrayOfFloat.construct(values=v[1]["values"])
            elif v[0].endswith("ArrayOfDouble"):
                return ArrayOfDouble.construct(values=v[1]["values"])
            elif v[0].endswith("ArrayOfString"):
                return ArrayOfString.construct(values=v[1]["values"])
        return v
