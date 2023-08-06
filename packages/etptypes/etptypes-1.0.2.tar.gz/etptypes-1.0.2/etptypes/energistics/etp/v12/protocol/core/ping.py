# -*- coding: utf-8 -*-

""" avro python class for file: ping """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Protocol.Core", "name": "Ping", "protocol": "0", "messageType": "8", "senderRole": "client,server", "protocolRoles": "client, server", "multipartFlag": false, "fields": [{"name": "currentDateTime", "type": "long"}], "fullName": "Energistics.Etp.v12.Protocol.Core.Ping", "depends": []}'


class Ping(ETPModel):

    current_date_time: int = Field(alias="currentDateTime")
