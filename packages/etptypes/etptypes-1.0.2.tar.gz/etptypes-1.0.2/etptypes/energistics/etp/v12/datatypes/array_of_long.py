# -*- coding: utf-8 -*-

""" avro python class for file: array_of_long """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "ArrayOfLong", "fields": [{"name": "values", "type": {"type": "array", "items": "long"}}], "fullName": "Energistics.Etp.v12.Datatypes.ArrayOfLong", "depends": []}'


class ArrayOfLong(ETPModel):

    values: typing.List[Strict[int]] = Field(alias="values")
