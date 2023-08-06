# -*- coding: utf-8 -*-

""" avro python class for file: find_data_objects """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


from etptypes.energistics.etp.v12.datatypes.object.context_info import ContextInfo

from etptypes.energistics.etp.v12.datatypes.object.context_scope_kind import (
    ContextScopeKind,
)

from etptypes.energistics.etp.v12.datatypes.object.active_status_kind import (
    ActiveStatusKind,
)


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Protocol.StoreQuery", "name": "FindDataObjects", "protocol": "14", "messageType": "1", "senderRole": "customer", "protocolRoles": "store,customer", "multipartFlag": false, "fields": [{"name": "context", "type": {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes.Object", "name": "ContextInfo", "fields": [{"name": "uri", "type": "string"}, {"name": "depth", "type": "int"}, {"name": "dataObjectTypes", "type": {"type": "array", "items": "string"}, "default": []}, {"name": "navigableEdges", "type": {"type": "enum", "namespace": "Energistics.Etp.v12.Datatypes.Object", "name": "RelationshipKind", "symbols": ["Primary", "Secondary", "Both"], "fullName": "Energistics.Etp.v12.Datatypes.Object.RelationshipKind", "depends": []}}, {"name": "includeSecondaryTargets", "type": "boolean", "default": false}, {"name": "includeSecondarySources", "type": "boolean", "default": false}], "fullName": "Energistics.Etp.v12.Datatypes.Object.ContextInfo", "depends": ["Energistics.Etp.v12.Datatypes.Object.RelationshipKind"]}}, {"name": "scope", "type": {"type": "enum", "namespace": "Energistics.Etp.v12.Datatypes.Object", "name": "ContextScopeKind", "symbols": ["self", "sources", "targets", "sourcesOrSelf", "targetsOrSelf"], "fullName": "Energistics.Etp.v12.Datatypes.Object.ContextScopeKind", "depends": []}}, {"name": "storeLastWriteFilter", "type": ["null", "long"]}, {"name": "activeStatusFilter", "type": ["null", {"type": "enum", "namespace": "Energistics.Etp.v12.Datatypes.Object", "name": "ActiveStatusKind", "symbols": ["Active", "Inactive"], "fullName": "Energistics.Etp.v12.Datatypes.Object.ActiveStatusKind", "depends": []}]}, {"name": "format", "type": "string", "default": "xml"}], "fullName": "Energistics.Etp.v12.Protocol.StoreQuery.FindDataObjects", "depends": ["Energistics.Etp.v12.Datatypes.Object.ContextInfo", "Energistics.Etp.v12.Datatypes.Object.ContextScopeKind", "Energistics.Etp.v12.Datatypes.Object.ActiveStatusKind"]}'


class FindDataObjects(ETPModel):

    context: ContextInfo = Field(alias="context")

    scope: ContextScopeKind = Field(alias="scope")

    store_last_write_filter: typing.Optional[Strict[int]] = Field(
        alias="storeLastWriteFilter"
    )

    active_status_filter: typing.Optional[ActiveStatusKind] = Field(
        alias="activeStatusFilter"
    )

    format_: str = Field(alias="format", default="xml")
