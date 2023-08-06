# -*- coding: utf-8 -*-

""" avro python class for file: array_of_nullable_long """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "ArrayOfNullableLong", "fields": [{"name": "values", "type": {"type": "array", "items": ["null", "long"]}}], "fullName": "Energistics.Etp.v12.Datatypes.ArrayOfNullableLong", "depends": []}'


class ArrayOfNullableLong(ETPModel):

    values: typing.List[typing.Optional[Strict[int]]] = Field(alias="values")
