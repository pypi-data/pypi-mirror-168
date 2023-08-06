# -*- coding: utf-8 -*-

""" avro python class for file: unsubscribe_channels """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Protocol.ChannelSubscribe", "name": "UnsubscribeChannels", "protocol": "21", "messageType": "7", "senderRole": "customer", "protocolRoles": "store,customer", "multipartFlag": false, "fields": [{"name": "channelIds", "type": {"type": "map", "values": "long"}}], "fullName": "Energistics.Etp.v12.Protocol.ChannelSubscribe.UnsubscribeChannels", "depends": []}'


class UnsubscribeChannels(ETPModel):

    channel_ids: typing.Mapping[str, int] = Field(alias="channelIds")
