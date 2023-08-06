# -*- coding: utf-8 -*-

""" avro python class for file: version """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "Version", "fields": [{"name": "major", "type": "int", "default": 0}, {"name": "minor", "type": "int", "default": 0}, {"name": "revision", "type": "int", "default": 0}, {"name": "patch", "type": "int", "default": 0}], "fullName": "Energistics.Etp.v12.Datatypes.Version", "depends": []}'


class Version(ETPModel):

    major: int = Field(alias="major", default=0)

    minor: int = Field(alias="minor", default=0)

    revision: int = Field(alias="revision", default=0)

    patch: int = Field(alias="patch", default=0)
