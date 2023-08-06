# -*- coding: utf-8 -*-

""" avro python class for file: truncate_channels_response """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Protocol.ChannelDataLoad", "name": "TruncateChannelsResponse", "protocol": "22", "messageType": "10", "senderRole": "store", "protocolRoles": "store,customer", "multipartFlag": true, "fields": [{"name": "channelsTruncatedTime", "type": {"type": "map", "values": "long"}}], "fullName": "Energistics.Etp.v12.Protocol.ChannelDataLoad.TruncateChannelsResponse", "depends": []}'


class TruncateChannelsResponse(ETPModel):

    channels_truncated_time: typing.Mapping[str, int] = Field(
        alias="channelsTruncatedTime"
    )
