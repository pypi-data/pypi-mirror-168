# -*- coding: utf-8 -*-

""" avro python class for file: get_supported_types """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


from etptypes.energistics.etp.v12.datatypes.object.context_scope_kind import (
    ContextScopeKind,
)


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Protocol.SupportedTypes", "name": "GetSupportedTypes", "protocol": "25", "messageType": "1", "senderRole": "customer", "protocolRoles": "store,customer", "multipartFlag": false, "fields": [{"name": "uri", "type": "string"}, {"name": "scope", "type": {"type": "enum", "namespace": "Energistics.Etp.v12.Datatypes.Object", "name": "ContextScopeKind", "symbols": ["self", "sources", "targets", "sourcesOrSelf", "targetsOrSelf"], "fullName": "Energistics.Etp.v12.Datatypes.Object.ContextScopeKind", "depends": []}}, {"name": "returnEmptyTypes", "type": "boolean", "default": false}, {"name": "countObjects", "type": "boolean", "default": false}], "fullName": "Energistics.Etp.v12.Protocol.SupportedTypes.GetSupportedTypes", "depends": ["Energistics.Etp.v12.Datatypes.Object.ContextScopeKind"]}'


class GetSupportedTypes(ETPModel):

    uri: str = Field(alias="uri")

    scope: ContextScopeKind = Field(alias="scope")

    return_empty_types: bool = Field(alias="returnEmptyTypes", default=False)

    count_objects: bool = Field(alias="countObjects", default=False)
