# -*- coding: utf-8 -*-

""" avro python class for file: data_array_identifier """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Datatypes.DataArrayTypes", "name": "DataArrayIdentifier", "fields": [{"name": "uri", "type": "string"}, {"name": "pathInResource", "type": "string"}], "fullName": "Energistics.Etp.v12.Datatypes.DataArrayTypes.DataArrayIdentifier", "depends": []}'


class DataArrayIdentifier(ETPModel):

    uri: str = Field(alias="uri")

    path_in_resource: str = Field(alias="pathInResource")
