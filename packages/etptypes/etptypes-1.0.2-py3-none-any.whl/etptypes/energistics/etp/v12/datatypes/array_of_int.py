# -*- coding: utf-8 -*-

""" avro python class for file: array_of_int """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "ArrayOfInt", "fields": [{"name": "values", "type": {"type": "array", "items": "int"}}], "fullName": "Energistics.Etp.v12.Datatypes.ArrayOfInt", "depends": []}'


class ArrayOfInt(ETPModel):

    values: typing.List[Strict[int]] = Field(alias="values")
