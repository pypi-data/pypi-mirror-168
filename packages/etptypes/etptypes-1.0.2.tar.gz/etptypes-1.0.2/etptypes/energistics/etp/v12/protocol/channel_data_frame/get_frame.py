# -*- coding: utf-8 -*-

""" avro python class for file: get_frame """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


from etptypes.energistics.etp.v12.datatypes.object.index_interval import IndexInterval

from etptypes.energistics.etp.v12.datatypes.uuid import Uuid


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Protocol.ChannelDataFrame", "name": "GetFrame", "protocol": "2", "messageType": "3", "senderRole": "customer", "protocolRoles": "store,customer", "multipartFlag": false, "fields": [{"name": "uri", "type": "string"}, {"name": "includeAllChannelSecondaryIndexes", "type": "boolean", "default": false}, {"name": "requestedInterval", "type": {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes.Object", "name": "IndexInterval", "fields": [{"name": "startIndex", "type": {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "IndexValue", "fields": [{"name": "item", "type": ["null", "long", "double", {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes.ChannelData", "name": "PassIndexedDepth", "fields": [{"name": "pass", "type": "long"}, {"name": "direction", "type": {"type": "enum", "namespace": "Energistics.Etp.v12.Datatypes.ChannelData", "name": "PassDirection", "symbols": ["Up", "HoldingSteady", "Down"], "fullName": "Energistics.Etp.v12.Datatypes.ChannelData.PassDirection", "depends": []}}, {"name": "depth", "type": "double"}], "fullName": "Energistics.Etp.v12.Datatypes.ChannelData.PassIndexedDepth", "depends": ["Energistics.Etp.v12.Datatypes.ChannelData.PassDirection"]}]}], "fullName": "Energistics.Etp.v12.Datatypes.IndexValue", "depends": ["Energistics.Etp.v12.Datatypes.ChannelData.PassIndexedDepth"]}}, {"name": "endIndex", "type": "Energistics.Etp.v12.Datatypes.IndexValue"}, {"name": "uom", "type": "string"}, {"name": "depthDatum", "type": "string", "default": ""}], "fullName": "Energistics.Etp.v12.Datatypes.Object.IndexInterval", "depends": ["Energistics.Etp.v12.Datatypes.IndexValue"]}}, {"name": "requestUuid", "type": {"type": "fixed", "namespace": "Energistics.Etp.v12.Datatypes", "name": "Uuid", "size": 16, "fullName": "Energistics.Etp.v12.Datatypes.Uuid", "depends": []}}, {"name": "requestedSecondaryIntervals", "type": {"type": "array", "items": "Energistics.Etp.v12.Datatypes.Object.IndexInterval"}, "default": []}], "fullName": "Energistics.Etp.v12.Protocol.ChannelDataFrame.GetFrame", "depends": ["Energistics.Etp.v12.Datatypes.Object.IndexInterval", "Energistics.Etp.v12.Datatypes.Uuid"]}'


class GetFrame(ETPModel):

    uri: str = Field(alias="uri")

    requested_interval: IndexInterval = Field(alias="requestedInterval")

    request_uuid: Uuid = Field(alias="requestUuid")

    include_all_channel_secondary_indexes: bool = Field(
        alias="includeAllChannelSecondaryIndexes", default=False
    )

    requested_secondary_intervals: typing.List[IndexInterval] = Field(
        alias="requestedSecondaryIntervals", default_factory=lambda: []
    )
