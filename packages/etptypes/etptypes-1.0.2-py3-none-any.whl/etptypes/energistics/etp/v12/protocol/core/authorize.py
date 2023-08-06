# -*- coding: utf-8 -*-

""" avro python class for file: authorize """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Protocol.Core", "name": "Authorize", "protocol": "0", "messageType": "6", "senderRole": "client,server", "protocolRoles": "client, server", "multipartFlag": false, "fields": [{"name": "authorization", "type": "string"}, {"name": "supplementalAuthorization", "type": {"type": "map", "values": "string"}}], "fullName": "Energistics.Etp.v12.Protocol.Core.Authorize", "depends": []}'


class Authorize(ETPModel):

    authorization: str = Field(alias="authorization")

    supplemental_authorization: typing.Mapping[str, str] = Field(
        alias="supplementalAuthorization"
    )
