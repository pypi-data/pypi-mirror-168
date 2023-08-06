# -*- coding: utf-8 -*-

""" avro python class for file: array_of_bytes """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "ArrayOfBytes", "fields": [{"name": "values", "type": {"type": "array", "items": "bytes"}}], "fullName": "Energistics.Etp.v12.Datatypes.ArrayOfBytes", "depends": []}'


class ArrayOfBytes(ETPModel):

    values: typing.List[Strict[bytes]] = Field(alias="values")
