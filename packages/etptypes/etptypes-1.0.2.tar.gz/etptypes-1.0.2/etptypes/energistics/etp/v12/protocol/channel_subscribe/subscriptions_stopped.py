# -*- coding: utf-8 -*-

""" avro python class for file: subscriptions_stopped """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Protocol.ChannelSubscribe", "name": "SubscriptionsStopped", "protocol": "21", "messageType": "8", "senderRole": "store", "protocolRoles": "store,customer", "multipartFlag": true, "fields": [{"name": "reason", "type": "string"}, {"name": "channelIds", "type": {"type": "map", "values": "long"}, "default": {}}], "fullName": "Energistics.Etp.v12.Protocol.ChannelSubscribe.SubscriptionsStopped", "depends": []}'


class SubscriptionsStopped(ETPModel):

    reason: str = Field(alias="reason")

    channel_ids: typing.Mapping[str, int] = Field(
        alias="channelIds", default_factory=lambda: {}
    )
