# -*- coding: utf-8 -*-

""" avro python class for file: subscribe_notifications """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


from etptypes.energistics.etp.v12.datatypes.object.subscription_info import (
    SubscriptionInfo,
)


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Protocol.StoreNotification", "name": "SubscribeNotifications", "protocol": "5", "messageType": "6", "senderRole": "customer", "protocolRoles": "store,customer", "multipartFlag": false, "fields": [{"name": "request", "type": {"type": "map", "values": {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes.Object", "name": "SubscriptionInfo", "fields": [{"name": "context", "type": {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes.Object", "name": "ContextInfo", "fields": [{"name": "uri", "type": "string"}, {"name": "depth", "type": "int"}, {"name": "dataObjectTypes", "type": {"type": "array", "items": "string"}, "default": []}, {"name": "navigableEdges", "type": {"type": "enum", "namespace": "Energistics.Etp.v12.Datatypes.Object", "name": "RelationshipKind", "symbols": ["Primary", "Secondary", "Both"], "fullName": "Energistics.Etp.v12.Datatypes.Object.RelationshipKind", "depends": []}}, {"name": "includeSecondaryTargets", "type": "boolean", "default": false}, {"name": "includeSecondarySources", "type": "boolean", "default": false}], "fullName": "Energistics.Etp.v12.Datatypes.Object.ContextInfo", "depends": ["Energistics.Etp.v12.Datatypes.Object.RelationshipKind"]}}, {"name": "scope", "type": {"type": "enum", "namespace": "Energistics.Etp.v12.Datatypes.Object", "name": "ContextScopeKind", "symbols": ["self", "sources", "targets", "sourcesOrSelf", "targetsOrSelf"], "fullName": "Energistics.Etp.v12.Datatypes.Object.ContextScopeKind", "depends": []}}, {"name": "requestUuid", "type": {"type": "fixed", "namespace": "Energistics.Etp.v12.Datatypes", "name": "Uuid", "size": 16, "fullName": "Energistics.Etp.v12.Datatypes.Uuid", "depends": []}}, {"name": "includeObjectData", "type": "boolean"}, {"name": "format", "type": "string", "default": "xml"}], "fullName": "Energistics.Etp.v12.Datatypes.Object.SubscriptionInfo", "depends": ["Energistics.Etp.v12.Datatypes.Object.ContextInfo", "Energistics.Etp.v12.Datatypes.Object.ContextScopeKind", "Energistics.Etp.v12.Datatypes.Uuid"]}}}], "fullName": "Energistics.Etp.v12.Protocol.StoreNotification.SubscribeNotifications", "depends": ["Energistics.Etp.v12.Datatypes.Object.SubscriptionInfo"]}'


class SubscribeNotifications(ETPModel):

    request: typing.Mapping[str, SubscriptionInfo] = Field(alias="request")
