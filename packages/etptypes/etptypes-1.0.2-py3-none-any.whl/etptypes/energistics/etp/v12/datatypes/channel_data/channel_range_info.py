# -*- coding: utf-8 -*-

""" avro python class for file: channel_range_info """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


from etptypes.energistics.etp.v12.datatypes.object.index_interval import IndexInterval


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Datatypes.ChannelData", "name": "ChannelRangeInfo", "fields": [{"name": "channelIds", "type": {"type": "array", "items": "long"}}, {"name": "interval", "type": {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes.Object", "name": "IndexInterval", "fields": [{"name": "startIndex", "type": {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "IndexValue", "fields": [{"name": "item", "type": ["null", "long", "double", {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes.ChannelData", "name": "PassIndexedDepth", "fields": [{"name": "pass", "type": "long"}, {"name": "direction", "type": {"type": "enum", "namespace": "Energistics.Etp.v12.Datatypes.ChannelData", "name": "PassDirection", "symbols": ["Up", "HoldingSteady", "Down"], "fullName": "Energistics.Etp.v12.Datatypes.ChannelData.PassDirection", "depends": []}}, {"name": "depth", "type": "double"}], "fullName": "Energistics.Etp.v12.Datatypes.ChannelData.PassIndexedDepth", "depends": ["Energistics.Etp.v12.Datatypes.ChannelData.PassDirection"]}]}], "fullName": "Energistics.Etp.v12.Datatypes.IndexValue", "depends": ["Energistics.Etp.v12.Datatypes.ChannelData.PassIndexedDepth"]}}, {"name": "endIndex", "type": "Energistics.Etp.v12.Datatypes.IndexValue"}, {"name": "uom", "type": "string"}, {"name": "depthDatum", "type": "string", "default": ""}], "fullName": "Energistics.Etp.v12.Datatypes.Object.IndexInterval", "depends": ["Energistics.Etp.v12.Datatypes.IndexValue"]}}, {"name": "secondaryIntervals", "type": {"type": "array", "items": "Energistics.Etp.v12.Datatypes.Object.IndexInterval"}, "default": []}], "fullName": "Energistics.Etp.v12.Datatypes.ChannelData.ChannelRangeInfo", "depends": ["Energistics.Etp.v12.Datatypes.Object.IndexInterval"]}'


class ChannelRangeInfo(ETPModel):

    channel_ids: typing.List[Strict[int]] = Field(alias="channelIds")

    interval: IndexInterval = Field(alias="interval")

    secondary_intervals: typing.List[IndexInterval] = Field(
        alias="secondaryIntervals", default_factory=lambda: []
    )
