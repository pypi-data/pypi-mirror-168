# -*- coding: utf-8 -*-

""" avro python class for file: channel_subscribe_info """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


from etptypes.energistics.etp.v12.datatypes.index_value import IndexValue


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Datatypes.ChannelData", "name": "ChannelSubscribeInfo", "fields": [{"name": "channelId", "type": "long"}, {"name": "startIndex", "type": {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "IndexValue", "fields": [{"name": "item", "type": ["null", "long", "double", {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes.ChannelData", "name": "PassIndexedDepth", "fields": [{"name": "pass", "type": "long"}, {"name": "direction", "type": {"type": "enum", "namespace": "Energistics.Etp.v12.Datatypes.ChannelData", "name": "PassDirection", "symbols": ["Up", "HoldingSteady", "Down"], "fullName": "Energistics.Etp.v12.Datatypes.ChannelData.PassDirection", "depends": []}}, {"name": "depth", "type": "double"}], "fullName": "Energistics.Etp.v12.Datatypes.ChannelData.PassIndexedDepth", "depends": ["Energistics.Etp.v12.Datatypes.ChannelData.PassDirection"]}]}], "fullName": "Energistics.Etp.v12.Datatypes.IndexValue", "depends": ["Energistics.Etp.v12.Datatypes.ChannelData.PassIndexedDepth"]}}, {"name": "dataChanges", "type": "boolean", "default": true}, {"name": "requestLatestIndexCount", "type": ["null", "int"]}], "fullName": "Energistics.Etp.v12.Datatypes.ChannelData.ChannelSubscribeInfo", "depends": ["Energistics.Etp.v12.Datatypes.IndexValue"]}'


class ChannelSubscribeInfo(ETPModel):

    channel_id: int = Field(alias="channelId")

    start_index: IndexValue = Field(alias="startIndex")

    request_latest_index_count: typing.Optional[Strict[int]] = Field(
        alias="requestLatestIndexCount"
    )

    data_changes: bool = Field(alias="dataChanges", default=True)
