# -*- coding: utf-8 -*-

""" avro python class for file: error_info """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "ErrorInfo", "fields": [{"name": "message", "type": "string"}, {"name": "code", "type": "int"}], "fullName": "Energistics.Etp.v12.Datatypes.ErrorInfo", "depends": []}'


class ErrorInfo(ETPModel):

    message: str = Field(alias="message")

    code: int = Field(alias="code")
