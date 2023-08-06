# -*- coding: utf-8 -*-

""" avro python class for file: close_session """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Protocol.Core", "name": "CloseSession", "protocol": "0", "messageType": "5", "senderRole": "client,server", "protocolRoles": "client, server", "multipartFlag": false, "fields": [{"name": "reason", "type": "string", "default": ""}], "fullName": "Energistics.Etp.v12.Protocol.Core.CloseSession", "depends": []}'


class CloseSession(ETPModel):

    reason: str = Field(alias="reason", default="")
