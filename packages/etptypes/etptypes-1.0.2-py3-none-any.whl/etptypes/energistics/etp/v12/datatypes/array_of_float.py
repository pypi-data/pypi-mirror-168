# -*- coding: utf-8 -*-

""" avro python class for file: array_of_float """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "ArrayOfFloat", "fields": [{"name": "values", "type": {"type": "array", "items": "float"}}], "fullName": "Energistics.Etp.v12.Datatypes.ArrayOfFloat", "depends": []}'


class ArrayOfFloat(ETPModel):

    values: typing.List[Strict[float]] = Field(alias="values")
