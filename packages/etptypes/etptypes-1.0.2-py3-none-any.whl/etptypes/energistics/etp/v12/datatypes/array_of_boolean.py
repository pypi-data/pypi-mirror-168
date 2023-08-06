# -*- coding: utf-8 -*-

""" avro python class for file: array_of_boolean """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "ArrayOfBoolean", "fields": [{"name": "values", "type": {"type": "array", "items": "boolean"}}], "fullName": "Energistics.Etp.v12.Datatypes.ArrayOfBoolean", "depends": []}'


class ArrayOfBoolean(ETPModel):

    values: typing.List[Strict[bool]] = Field(alias="values")
