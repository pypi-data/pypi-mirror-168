# -*- coding: utf-8 -*-

""" avro python class for file: pong """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Protocol.Core", "name": "Pong", "protocol": "0", "messageType": "9", "senderRole": "client,server", "protocolRoles": "client, server", "multipartFlag": false, "fields": [{"name": "currentDateTime", "type": "long"}], "fullName": "Energistics.Etp.v12.Protocol.Core.Pong", "depends": []}'


class Pong(ETPModel):

    current_date_time: int = Field(alias="currentDateTime")
