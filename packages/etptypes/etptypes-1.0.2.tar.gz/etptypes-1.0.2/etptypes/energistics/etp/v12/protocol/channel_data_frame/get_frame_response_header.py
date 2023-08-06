# -*- coding: utf-8 -*-

""" avro python class for file: get_frame_response_header """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


from etptypes.energistics.etp.v12.datatypes.channel_data.index_metadata_record import (
    IndexMetadataRecord,
)


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Protocol.ChannelDataFrame", "name": "GetFrameResponseHeader", "protocol": "2", "messageType": "4", "senderRole": "store", "protocolRoles": "store,customer", "multipartFlag": true, "fields": [{"name": "channelUris", "type": {"type": "array", "items": "string"}}, {"name": "indexes", "type": {"type": "array", "items": {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes.ChannelData", "name": "IndexMetadataRecord", "fields": [{"name": "indexKind", "type": {"type": "enum", "namespace": "Energistics.Etp.v12.Datatypes.ChannelData", "name": "ChannelIndexKind", "symbols": ["DateTime", "ElapsedTime", "MeasuredDepth", "TrueVerticalDepth", "PassIndexedDepth", "Pressure", "Temperature", "Scalar"], "fullName": "Energistics.Etp.v12.Datatypes.ChannelData.ChannelIndexKind", "depends": []}, "default": "DateTime"}, {"name": "interval", "type": {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes.Object", "name": "IndexInterval", "fields": [{"name": "startIndex", "type": {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "IndexValue", "fields": [{"name": "item", "type": ["null", "long", "double", {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes.ChannelData", "name": "PassIndexedDepth", "fields": [{"name": "pass", "type": "long"}, {"name": "direction", "type": {"type": "enum", "namespace": "Energistics.Etp.v12.Datatypes.ChannelData", "name": "PassDirection", "symbols": ["Up", "HoldingSteady", "Down"], "fullName": "Energistics.Etp.v12.Datatypes.ChannelData.PassDirection", "depends": []}}, {"name": "depth", "type": "double"}], "fullName": "Energistics.Etp.v12.Datatypes.ChannelData.PassIndexedDepth", "depends": ["Energistics.Etp.v12.Datatypes.ChannelData.PassDirection"]}]}], "fullName": "Energistics.Etp.v12.Datatypes.IndexValue", "depends": ["Energistics.Etp.v12.Datatypes.ChannelData.PassIndexedDepth"]}}, {"name": "endIndex", "type": "Energistics.Etp.v12.Datatypes.IndexValue"}, {"name": "uom", "type": "string"}, {"name": "depthDatum", "type": "string", "default": ""}], "fullName": "Energistics.Etp.v12.Datatypes.Object.IndexInterval", "depends": ["Energistics.Etp.v12.Datatypes.IndexValue"]}}, {"name": "direction", "type": {"type": "enum", "namespace": "Energistics.Etp.v12.Datatypes.ChannelData", "name": "IndexDirection", "symbols": ["Increasing", "Decreasing", "Unordered"], "fullName": "Energistics.Etp.v12.Datatypes.ChannelData.IndexDirection", "depends": []}, "default": "Increasing"}, {"name": "name", "type": "string", "default": ""}, {"name": "uom", "type": "string"}, {"name": "depthDatum", "type": "string", "default": ""}, {"name": "indexPropertyKindUri", "type": "string"}, {"name": "filterable", "type": "boolean", "default": true}], "fullName": "Energistics.Etp.v12.Datatypes.ChannelData.IndexMetadataRecord", "depends": ["Energistics.Etp.v12.Datatypes.ChannelData.ChannelIndexKind", "Energistics.Etp.v12.Datatypes.Object.IndexInterval", "Energistics.Etp.v12.Datatypes.ChannelData.IndexDirection"]}}}], "fullName": "Energistics.Etp.v12.Protocol.ChannelDataFrame.GetFrameResponseHeader", "depends": ["Energistics.Etp.v12.Datatypes.ChannelData.IndexMetadataRecord"]}'


class GetFrameResponseHeader(ETPModel):

    channel_uris: typing.List[Strict[str]] = Field(alias="channelUris")

    indexes: typing.List[IndexMetadataRecord] = Field(alias="indexes")
