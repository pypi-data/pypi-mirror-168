# -*- coding: utf-8 -*-

""" avro python class for file: array_of_double """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "ArrayOfDouble", "fields": [{"name": "values", "type": {"type": "array", "items": "double"}}], "fullName": "Energistics.Etp.v12.Datatypes.ArrayOfDouble", "depends": []}'


class ArrayOfDouble(ETPModel):

    values: typing.List[Strict[float]] = Field(alias="values")
