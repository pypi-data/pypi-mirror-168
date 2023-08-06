# -*- coding: utf-8 -*-

""" avro python class for file: array_of_string """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "ArrayOfString", "fields": [{"name": "values", "type": {"type": "array", "items": "string"}}], "fullName": "Energistics.Etp.v12.Datatypes.ArrayOfString", "depends": []}'


class ArrayOfString(ETPModel):

    values: typing.List[Strict[str]] = Field(alias="values")
