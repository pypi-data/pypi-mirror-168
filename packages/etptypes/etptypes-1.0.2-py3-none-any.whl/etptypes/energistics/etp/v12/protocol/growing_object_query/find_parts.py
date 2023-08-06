# -*- coding: utf-8 -*-

""" avro python class for file: find_parts """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Protocol.GrowingObjectQuery", "name": "FindParts", "protocol": "16", "messageType": "1", "senderRole": "customer", "protocolRoles": "store,customer", "multipartFlag": false, "fields": [{"name": "uri", "type": "string"}, {"name": "format", "type": "string", "default": "xml"}], "fullName": "Energistics.Etp.v12.Protocol.GrowingObjectQuery.FindParts", "depends": []}'


class FindParts(ETPModel):

    uri: str = Field(alias="uri")

    format_: str = Field(alias="format", default="xml")
