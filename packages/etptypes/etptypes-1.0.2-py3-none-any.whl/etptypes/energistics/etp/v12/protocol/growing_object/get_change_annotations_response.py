# -*- coding: utf-8 -*-

""" avro python class for file: get_change_annotations_response """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


from etptypes.energistics.etp.v12.datatypes.object.change_response_info import (
    ChangeResponseInfo,
)


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Protocol.GrowingObject", "name": "GetChangeAnnotationsResponse", "protocol": "6", "messageType": "20", "senderRole": "store", "protocolRoles": "store,customer", "multipartFlag": true, "fields": [{"name": "changes", "type": {"type": "map", "values": {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes.Object", "name": "ChangeResponseInfo", "fields": [{"name": "responseTimestamp", "type": "long"}, {"name": "changes", "type": {"type": "map", "values": {"type": "array", "items": {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes.Object", "name": "ChangeAnnotation", "fields": [{"name": "changeTime", "type": "long"}, {"name": "interval", "type": {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes.Object", "name": "IndexInterval", "fields": [{"name": "startIndex", "type": {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "IndexValue", "fields": [{"name": "item", "type": ["null", "long", "double", {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes.ChannelData", "name": "PassIndexedDepth", "fields": [{"name": "pass", "type": "long"}, {"name": "direction", "type": {"type": "enum", "namespace": "Energistics.Etp.v12.Datatypes.ChannelData", "name": "PassDirection", "symbols": ["Up", "HoldingSteady", "Down"], "fullName": "Energistics.Etp.v12.Datatypes.ChannelData.PassDirection", "depends": []}}, {"name": "depth", "type": "double"}], "fullName": "Energistics.Etp.v12.Datatypes.ChannelData.PassIndexedDepth", "depends": ["Energistics.Etp.v12.Datatypes.ChannelData.PassDirection"]}]}], "fullName": "Energistics.Etp.v12.Datatypes.IndexValue", "depends": ["Energistics.Etp.v12.Datatypes.ChannelData.PassIndexedDepth"]}}, {"name": "endIndex", "type": "Energistics.Etp.v12.Datatypes.IndexValue"}, {"name": "uom", "type": "string"}, {"name": "depthDatum", "type": "string", "default": ""}], "fullName": "Energistics.Etp.v12.Datatypes.Object.IndexInterval", "depends": ["Energistics.Etp.v12.Datatypes.IndexValue"]}}], "fullName": "Energistics.Etp.v12.Datatypes.Object.ChangeAnnotation", "depends": ["Energistics.Etp.v12.Datatypes.Object.IndexInterval"]}}}}], "fullName": "Energistics.Etp.v12.Datatypes.Object.ChangeResponseInfo", "depends": ["Energistics.Etp.v12.Datatypes.Object.ChangeAnnotation"]}}}], "fullName": "Energistics.Etp.v12.Protocol.GrowingObject.GetChangeAnnotationsResponse", "depends": ["Energistics.Etp.v12.Datatypes.Object.ChangeResponseInfo"]}'


class GetChangeAnnotationsResponse(ETPModel):

    changes: typing.Mapping[str, ChangeResponseInfo] = Field(alias="changes")
