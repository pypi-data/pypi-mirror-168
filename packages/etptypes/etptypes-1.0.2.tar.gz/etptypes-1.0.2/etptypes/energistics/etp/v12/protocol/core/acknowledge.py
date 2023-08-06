# -*- coding: utf-8 -*-

""" avro python class for file: acknowledge """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Protocol.Core", "name": "Acknowledge", "protocol": "0", "messageType": "1001", "senderRole": "*", "protocolRoles": "client, server", "multipartFlag": false, "fields": [], "fullName": "Energistics.Etp.v12.Protocol.Core.Acknowledge", "depends": []}'


class Acknowledge(ETPModel):
    pass
