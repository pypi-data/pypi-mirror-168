# -*- coding: utf-8 -*-

""" avro python class for file: authorize_response """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Protocol.Core", "name": "AuthorizeResponse", "protocol": "0", "messageType": "7", "senderRole": "client,server", "protocolRoles": "client, server", "multipartFlag": false, "fields": [{"name": "success", "type": "boolean"}, {"name": "challenges", "type": {"type": "array", "items": "string"}}], "fullName": "Energistics.Etp.v12.Protocol.Core.AuthorizeResponse", "depends": []}'


class AuthorizeResponse(ETPModel):

    success: bool = Field(alias="success")

    challenges: typing.List[Strict[str]] = Field(alias="challenges")
