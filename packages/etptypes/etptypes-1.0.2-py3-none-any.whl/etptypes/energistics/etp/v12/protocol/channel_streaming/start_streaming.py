# -*- coding: utf-8 -*-

""" avro python class for file: start_streaming """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Protocol.ChannelStreaming", "name": "StartStreaming", "protocol": "1", "messageType": "3", "senderRole": "consumer", "protocolRoles": "producer,consumer", "multipartFlag": false, "fields": [], "fullName": "Energistics.Etp.v12.Protocol.ChannelStreaming.StartStreaming", "depends": []}'


class StartStreaming(ETPModel):
    pass
