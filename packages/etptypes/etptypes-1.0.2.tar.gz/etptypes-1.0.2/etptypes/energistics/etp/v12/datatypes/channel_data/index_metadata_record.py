# -*- coding: utf-8 -*-

""" avro python class for file: index_metadata_record """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


from etptypes.energistics.etp.v12.datatypes.channel_data.channel_index_kind import (
    ChannelIndexKind,
)

from etptypes.energistics.etp.v12.datatypes.object.index_interval import IndexInterval

from etptypes.energistics.etp.v12.datatypes.channel_data.index_direction import (
    IndexDirection,
)


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Datatypes.ChannelData", "name": "IndexMetadataRecord", "fields": [{"name": "indexKind", "type": {"type": "enum", "namespace": "Energistics.Etp.v12.Datatypes.ChannelData", "name": "ChannelIndexKind", "symbols": ["DateTime", "ElapsedTime", "MeasuredDepth", "TrueVerticalDepth", "PassIndexedDepth", "Pressure", "Temperature", "Scalar"], "fullName": "Energistics.Etp.v12.Datatypes.ChannelData.ChannelIndexKind", "depends": []}, "default": "DateTime"}, {"name": "interval", "type": {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes.Object", "name": "IndexInterval", "fields": [{"name": "startIndex", "type": {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "IndexValue", "fields": [{"name": "item", "type": ["null", "long", "double", {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes.ChannelData", "name": "PassIndexedDepth", "fields": [{"name": "pass", "type": "long"}, {"name": "direction", "type": {"type": "enum", "namespace": "Energistics.Etp.v12.Datatypes.ChannelData", "name": "PassDirection", "symbols": ["Up", "HoldingSteady", "Down"], "fullName": "Energistics.Etp.v12.Datatypes.ChannelData.PassDirection", "depends": []}}, {"name": "depth", "type": "double"}], "fullName": "Energistics.Etp.v12.Datatypes.ChannelData.PassIndexedDepth", "depends": ["Energistics.Etp.v12.Datatypes.ChannelData.PassDirection"]}]}], "fullName": "Energistics.Etp.v12.Datatypes.IndexValue", "depends": ["Energistics.Etp.v12.Datatypes.ChannelData.PassIndexedDepth"]}}, {"name": "endIndex", "type": "Energistics.Etp.v12.Datatypes.IndexValue"}, {"name": "uom", "type": "string"}, {"name": "depthDatum", "type": "string", "default": ""}], "fullName": "Energistics.Etp.v12.Datatypes.Object.IndexInterval", "depends": ["Energistics.Etp.v12.Datatypes.IndexValue"]}}, {"name": "direction", "type": {"type": "enum", "namespace": "Energistics.Etp.v12.Datatypes.ChannelData", "name": "IndexDirection", "symbols": ["Increasing", "Decreasing", "Unordered"], "fullName": "Energistics.Etp.v12.Datatypes.ChannelData.IndexDirection", "depends": []}, "default": "Increasing"}, {"name": "name", "type": "string", "default": ""}, {"name": "uom", "type": "string"}, {"name": "depthDatum", "type": "string", "default": ""}, {"name": "indexPropertyKindUri", "type": "string"}, {"name": "filterable", "type": "boolean", "default": true}], "fullName": "Energistics.Etp.v12.Datatypes.ChannelData.IndexMetadataRecord", "depends": ["Energistics.Etp.v12.Datatypes.ChannelData.ChannelIndexKind", "Energistics.Etp.v12.Datatypes.Object.IndexInterval", "Energistics.Etp.v12.Datatypes.ChannelData.IndexDirection"]}'


class IndexMetadataRecord(ETPModel):

    interval: IndexInterval = Field(alias="interval")

    uom: str = Field(alias="uom")

    index_property_kind_uri: str = Field(alias="indexPropertyKindUri")

    index_kind: ChannelIndexKind = Field(alias="indexKind")

    direction: IndexDirection = Field(alias="direction")

    name: str = Field(alias="name", default="")

    depth_datum: str = Field(alias="depthDatum", default="")

    filterable: bool = Field(alias="filterable", default=True)
