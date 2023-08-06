# -*- coding: utf-8 -*-

""" avro python class for file: subscribe_channels_response """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Protocol.ChannelSubscribe", "name": "SubscribeChannelsResponse", "protocol": "21", "messageType": "12", "senderRole": "store", "protocolRoles": "store,customer", "multipartFlag": true, "fields": [{"name": "success", "type": {"type": "map", "values": "string"}}], "fullName": "Energistics.Etp.v12.Protocol.ChannelSubscribe.SubscribeChannelsResponse", "depends": []}'


class SubscribeChannelsResponse(ETPModel):

    success: typing.Mapping[str, str] = Field(alias="success")
