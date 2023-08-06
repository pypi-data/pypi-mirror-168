# -*- coding: utf-8 -*-

""" avro python class for file: open_channels """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Protocol.ChannelDataLoad", "name": "OpenChannels", "protocol": "22", "messageType": "1", "senderRole": "customer", "protocolRoles": "store,customer", "multipartFlag": false, "fields": [{"name": "uris", "type": {"type": "map", "values": "string"}}], "fullName": "Energistics.Etp.v12.Protocol.ChannelDataLoad.OpenChannels", "depends": []}'


class OpenChannels(ETPModel):

    uris: typing.Mapping[str, str] = Field(alias="uris")
