# -*- coding: utf-8 -*-

""" avro python class for file: close_channels """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Protocol.ChannelDataLoad", "name": "CloseChannels", "protocol": "22", "messageType": "3", "senderRole": "customer", "protocolRoles": "store,customer", "multipartFlag": false, "fields": [{"name": "id", "type": {"type": "map", "values": "long"}}], "fullName": "Energistics.Etp.v12.Protocol.ChannelDataLoad.CloseChannels", "depends": []}'


class CloseChannels(ETPModel):

    id_: typing.Mapping[str, int] = Field(alias="id")
