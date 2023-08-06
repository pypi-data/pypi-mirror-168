# -*- coding: utf-8 -*-

""" avro python class for file: get_supported_types_response """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


from etptypes.energistics.etp.v12.datatypes.object.supported_type import SupportedType


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Protocol.SupportedTypes", "name": "GetSupportedTypesResponse", "protocol": "25", "messageType": "2", "senderRole": "store", "protocolRoles": "store,customer", "multipartFlag": true, "fields": [{"name": "supportedTypes", "type": {"type": "array", "items": {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes.Object", "name": "SupportedType", "fields": [{"name": "dataObjectType", "type": "string"}, {"name": "objectCount", "type": ["null", "int"]}, {"name": "relationshipKind", "type": {"type": "enum", "namespace": "Energistics.Etp.v12.Datatypes.Object", "name": "RelationshipKind", "symbols": ["Primary", "Secondary", "Both"], "fullName": "Energistics.Etp.v12.Datatypes.Object.RelationshipKind", "depends": []}}], "fullName": "Energistics.Etp.v12.Datatypes.Object.SupportedType", "depends": ["Energistics.Etp.v12.Datatypes.Object.RelationshipKind"]}}, "default": []}], "fullName": "Energistics.Etp.v12.Protocol.SupportedTypes.GetSupportedTypesResponse", "depends": ["Energistics.Etp.v12.Datatypes.Object.SupportedType"]}'


class GetSupportedTypesResponse(ETPModel):

    supported_types: typing.List[SupportedType] = Field(
        alias="supportedTypes", default_factory=lambda: []
    )
