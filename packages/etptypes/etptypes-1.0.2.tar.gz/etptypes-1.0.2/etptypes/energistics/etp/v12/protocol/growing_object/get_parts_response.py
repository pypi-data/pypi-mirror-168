# -*- coding: utf-8 -*-

""" avro python class for file: get_parts_response """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


from etptypes.energistics.etp.v12.datatypes.object.object_part import ObjectPart


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Protocol.GrowingObject", "name": "GetPartsResponse", "protocol": "6", "messageType": "6", "senderRole": "store", "protocolRoles": "store,customer", "multipartFlag": true, "fields": [{"name": "uri", "type": "string"}, {"name": "format", "type": "string", "default": "xml"}, {"name": "parts", "type": {"type": "map", "values": {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes.Object", "name": "ObjectPart", "fields": [{"name": "uid", "type": "string"}, {"name": "data", "type": "bytes"}], "fullName": "Energistics.Etp.v12.Datatypes.Object.ObjectPart", "depends": []}}}], "fullName": "Energistics.Etp.v12.Protocol.GrowingObject.GetPartsResponse", "depends": ["Energistics.Etp.v12.Datatypes.Object.ObjectPart"]}'


class GetPartsResponse(ETPModel):

    uri: str = Field(alias="uri")

    parts: typing.Mapping[str, ObjectPart] = Field(alias="parts")

    format_: str = Field(alias="format", default="xml")
