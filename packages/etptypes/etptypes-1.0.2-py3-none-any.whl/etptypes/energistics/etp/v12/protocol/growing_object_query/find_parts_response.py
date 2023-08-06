# -*- coding: utf-8 -*-

""" avro python class for file: find_parts_response """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


from etptypes.energistics.etp.v12.datatypes.object.object_part import ObjectPart


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Protocol.GrowingObjectQuery", "name": "FindPartsResponse", "protocol": "16", "messageType": "2", "senderRole": "store", "protocolRoles": "store,customer", "multipartFlag": true, "fields": [{"name": "uri", "type": "string"}, {"name": "serverSortOrder", "type": "string"}, {"name": "format", "type": "string", "default": "xml"}, {"name": "parts", "type": {"type": "array", "items": {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes.Object", "name": "ObjectPart", "fields": [{"name": "uid", "type": "string"}, {"name": "data", "type": "bytes"}], "fullName": "Energistics.Etp.v12.Datatypes.Object.ObjectPart", "depends": []}}, "default": []}], "fullName": "Energistics.Etp.v12.Protocol.GrowingObjectQuery.FindPartsResponse", "depends": ["Energistics.Etp.v12.Datatypes.Object.ObjectPart"]}'


class FindPartsResponse(ETPModel):

    uri: str = Field(alias="uri")

    server_sort_order: str = Field(alias="serverSortOrder")

    format_: str = Field(alias="format", default="xml")

    parts: typing.List[ObjectPart] = Field(alias="parts", default_factory=lambda: [])
