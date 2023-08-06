# -*- coding: utf-8 -*-

""" avro python class for file: get_channel_metadata """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Protocol.ChannelSubscribe", "name": "GetChannelMetadata", "protocol": "21", "messageType": "1", "senderRole": "customer", "protocolRoles": "store,customer", "multipartFlag": false, "fields": [{"name": "uris", "type": {"type": "map", "values": "string"}}], "fullName": "Energistics.Etp.v12.Protocol.ChannelSubscribe.GetChannelMetadata", "depends": []}'


class GetChannelMetadata(ETPModel):

    uris: typing.Mapping[str, str] = Field(alias="uris")
