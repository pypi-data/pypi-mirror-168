# -*- coding: utf-8 -*-

""" avro python class for file: array_of_nullable_int """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "ArrayOfNullableInt", "fields": [{"name": "values", "type": {"type": "array", "items": ["null", "int"]}}], "fullName": "Energistics.Etp.v12.Datatypes.ArrayOfNullableInt", "depends": []}'


class ArrayOfNullableInt(ETPModel):

    values: typing.List[typing.Optional[Strict[int]]] = Field(alias="values")
