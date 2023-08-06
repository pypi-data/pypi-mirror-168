# -*- coding: utf-8 -*-

""" avro python class for file: replace_parts_by_range """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


from etptypes.energistics.etp.v12.datatypes.object.index_interval import IndexInterval

from etptypes.energistics.etp.v12.datatypes.object.object_part import ObjectPart


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Protocol.GrowingObject", "name": "ReplacePartsByRange", "protocol": "6", "messageType": "7", "senderRole": "customer", "protocolRoles": "store,customer", "multipartFlag": true, "fields": [{"name": "uri", "type": "string"}, {"name": "deleteInterval", "type": {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes.Object", "name": "IndexInterval", "fields": [{"name": "startIndex", "type": {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "IndexValue", "fields": [{"name": "item", "type": ["null", "long", "double", {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes.ChannelData", "name": "PassIndexedDepth", "fields": [{"name": "pass", "type": "long"}, {"name": "direction", "type": {"type": "enum", "namespace": "Energistics.Etp.v12.Datatypes.ChannelData", "name": "PassDirection", "symbols": ["Up", "HoldingSteady", "Down"], "fullName": "Energistics.Etp.v12.Datatypes.ChannelData.PassDirection", "depends": []}}, {"name": "depth", "type": "double"}], "fullName": "Energistics.Etp.v12.Datatypes.ChannelData.PassIndexedDepth", "depends": ["Energistics.Etp.v12.Datatypes.ChannelData.PassDirection"]}]}], "fullName": "Energistics.Etp.v12.Datatypes.IndexValue", "depends": ["Energistics.Etp.v12.Datatypes.ChannelData.PassIndexedDepth"]}}, {"name": "endIndex", "type": "Energistics.Etp.v12.Datatypes.IndexValue"}, {"name": "uom", "type": "string"}, {"name": "depthDatum", "type": "string", "default": ""}], "fullName": "Energistics.Etp.v12.Datatypes.Object.IndexInterval", "depends": ["Energistics.Etp.v12.Datatypes.IndexValue"]}}, {"name": "includeOverlappingIntervals", "type": "boolean"}, {"name": "format", "type": "string", "default": "xml"}, {"name": "parts", "type": {"type": "array", "items": {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes.Object", "name": "ObjectPart", "fields": [{"name": "uid", "type": "string"}, {"name": "data", "type": "bytes"}], "fullName": "Energistics.Etp.v12.Datatypes.Object.ObjectPart", "depends": []}}}], "fullName": "Energistics.Etp.v12.Protocol.GrowingObject.ReplacePartsByRange", "depends": ["Energistics.Etp.v12.Datatypes.Object.IndexInterval", "Energistics.Etp.v12.Datatypes.Object.ObjectPart"]}'


class ReplacePartsByRange(ETPModel):

    uri: str = Field(alias="uri")

    delete_interval: IndexInterval = Field(alias="deleteInterval")

    include_overlapping_intervals: bool = Field(alias="includeOverlappingIntervals")

    parts: typing.List[ObjectPart] = Field(alias="parts")

    format_: str = Field(alias="format", default="xml")
