# -*- coding: utf-8 -*-

""" avro python class for file: get_frame_metadata """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Protocol.ChannelDataFrame", "name": "GetFrameMetadata", "protocol": "2", "messageType": "1", "senderRole": "customer", "protocolRoles": "store,customer", "multipartFlag": false, "fields": [{"name": "uri", "type": "string"}, {"name": "includeAllChannelSecondaryIndexes", "type": "boolean", "default": false}], "fullName": "Energistics.Etp.v12.Protocol.ChannelDataFrame.GetFrameMetadata", "depends": []}'


class GetFrameMetadata(ETPModel):

    uri: str = Field(alias="uri")

    include_all_channel_secondary_indexes: bool = Field(
        alias="includeAllChannelSecondaryIndexes", default=False
    )
