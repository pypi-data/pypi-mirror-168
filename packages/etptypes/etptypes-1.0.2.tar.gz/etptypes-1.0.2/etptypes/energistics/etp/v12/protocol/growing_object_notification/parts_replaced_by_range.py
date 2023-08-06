# -*- coding: utf-8 -*-

""" avro python class for file: parts_replaced_by_range """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


from etptypes.energistics.etp.v12.datatypes.uuid import Uuid

from etptypes.energistics.etp.v12.datatypes.object.index_interval import IndexInterval

from etptypes.energistics.etp.v12.datatypes.object.object_part import ObjectPart


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Protocol.GrowingObjectNotification", "name": "PartsReplacedByRange", "protocol": "7", "messageType": "6", "senderRole": "store", "protocolRoles": "store,customer", "multipartFlag": true, "fields": [{"name": "uri", "type": "string"}, {"name": "requestUuid", "type": {"type": "fixed", "namespace": "Energistics.Etp.v12.Datatypes", "name": "Uuid", "size": 16, "fullName": "Energistics.Etp.v12.Datatypes.Uuid", "depends": []}}, {"name": "changeTime", "type": "long"}, {"name": "deletedInterval", "type": {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes.Object", "name": "IndexInterval", "fields": [{"name": "startIndex", "type": {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "IndexValue", "fields": [{"name": "item", "type": ["null", "long", "double", {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes.ChannelData", "name": "PassIndexedDepth", "fields": [{"name": "pass", "type": "long"}, {"name": "direction", "type": {"type": "enum", "namespace": "Energistics.Etp.v12.Datatypes.ChannelData", "name": "PassDirection", "symbols": ["Up", "HoldingSteady", "Down"], "fullName": "Energistics.Etp.v12.Datatypes.ChannelData.PassDirection", "depends": []}}, {"name": "depth", "type": "double"}], "fullName": "Energistics.Etp.v12.Datatypes.ChannelData.PassIndexedDepth", "depends": ["Energistics.Etp.v12.Datatypes.ChannelData.PassDirection"]}]}], "fullName": "Energistics.Etp.v12.Datatypes.IndexValue", "depends": ["Energistics.Etp.v12.Datatypes.ChannelData.PassIndexedDepth"]}}, {"name": "endIndex", "type": "Energistics.Etp.v12.Datatypes.IndexValue"}, {"name": "uom", "type": "string"}, {"name": "depthDatum", "type": "string", "default": ""}], "fullName": "Energistics.Etp.v12.Datatypes.Object.IndexInterval", "depends": ["Energistics.Etp.v12.Datatypes.IndexValue"]}}, {"name": "includeOverlappingIntervals", "type": "boolean"}, {"name": "format", "type": "string", "default": ""}, {"name": "parts", "type": {"type": "array", "items": {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes.Object", "name": "ObjectPart", "fields": [{"name": "uid", "type": "string"}, {"name": "data", "type": "bytes"}], "fullName": "Energistics.Etp.v12.Datatypes.Object.ObjectPart", "depends": []}}}], "fullName": "Energistics.Etp.v12.Protocol.GrowingObjectNotification.PartsReplacedByRange", "depends": ["Energistics.Etp.v12.Datatypes.Uuid", "Energistics.Etp.v12.Datatypes.Object.IndexInterval", "Energistics.Etp.v12.Datatypes.Object.ObjectPart"]}'


class PartsReplacedByRange(ETPModel):

    uri: str = Field(alias="uri")

    request_uuid: Uuid = Field(alias="requestUuid")

    change_time: int = Field(alias="changeTime")

    deleted_interval: IndexInterval = Field(alias="deletedInterval")

    include_overlapping_intervals: bool = Field(alias="includeOverlappingIntervals")

    parts: typing.List[ObjectPart] = Field(alias="parts")

    format_: str = Field(alias="format", default="")
