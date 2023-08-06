# -*- coding: utf-8 -*-

""" avro python class for file: any_array_type """

import typing
from pydantic import validator
from etptypes import StrEnum


avro_schema: typing.Final[
    str
] = '{"type": "enum", "namespace": "Energistics.Etp.v12.Datatypes", "name": "AnyArrayType", "symbols": ["arrayOfBoolean", "arrayOfInt", "arrayOfLong", "arrayOfFloat", "arrayOfDouble", "arrayOfString", "bytes"], "fullName": "Energistics.Etp.v12.Datatypes.AnyArrayType", "depends": []}'


class AnyArrayType(StrEnum):
    ARRAY_OF_BOOLEAN = "arrayOfBoolean"
    ARRAY_OF_INT = "arrayOfInt"
    ARRAY_OF_LONG = "arrayOfLong"
    ARRAY_OF_FLOAT = "arrayOfFloat"
    ARRAY_OF_DOUBLE = "arrayOfDouble"
    ARRAY_OF_STRING = "arrayOfString"
    BYTES = "bytes"
