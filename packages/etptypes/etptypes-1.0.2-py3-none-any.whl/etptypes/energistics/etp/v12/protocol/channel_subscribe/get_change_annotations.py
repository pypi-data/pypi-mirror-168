# -*- coding: utf-8 -*-

""" avro python class for file: get_change_annotations """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


from etptypes.energistics.etp.v12.datatypes.channel_data.channel_change_request_info import (
    ChannelChangeRequestInfo,
)


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Protocol.ChannelSubscribe", "name": "GetChangeAnnotations", "protocol": "21", "messageType": "14", "senderRole": "customer", "protocolRoles": "store,customer", "multipartFlag": false, "fields": [{"name": "channels", "type": {"type": "map", "values": {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes.ChannelData", "name": "ChannelChangeRequestInfo", "fields": [{"name": "sinceChangeTime", "type": "long"}, {"name": "channelIds", "type": {"type": "array", "items": "long"}}], "fullName": "Energistics.Etp.v12.Datatypes.ChannelData.ChannelChangeRequestInfo", "depends": []}}}, {"name": "latestOnly", "type": "boolean", "default": false}], "fullName": "Energistics.Etp.v12.Protocol.ChannelSubscribe.GetChangeAnnotations", "depends": ["Energistics.Etp.v12.Datatypes.ChannelData.ChannelChangeRequestInfo"]}'


class GetChangeAnnotations(ETPModel):

    channels: typing.Mapping[str, ChannelChangeRequestInfo] = Field(alias="channels")

    latest_only: bool = Field(alias="latestOnly", default=False)
