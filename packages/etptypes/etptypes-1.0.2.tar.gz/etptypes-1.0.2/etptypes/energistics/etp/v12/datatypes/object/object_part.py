# -*- coding: utf-8 -*-

""" avro python class for file: object_part """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Datatypes.Object", "name": "ObjectPart", "fields": [{"name": "uid", "type": "string"}, {"name": "data", "type": "bytes"}], "fullName": "Energistics.Etp.v12.Datatypes.Object.ObjectPart", "depends": []}'


class ObjectPart(ETPModel):

    uid: str = Field(alias="uid")

    data: bytes = Field(alias="data")
