# -*- coding: utf-8 -*-

""" avro python class for file: parts_changed """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


from etptypes.energistics.etp.v12.datatypes.uuid import Uuid

from etptypes.energistics.etp.v12.datatypes.object.object_change_kind import (
    ObjectChangeKind,
)

from etptypes.energistics.etp.v12.datatypes.object.object_part import ObjectPart


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Protocol.GrowingObjectNotification", "name": "PartsChanged", "protocol": "7", "messageType": "2", "senderRole": "store", "protocolRoles": "store,customer", "multipartFlag": false, "fields": [{"name": "uri", "type": "string"}, {"name": "requestUuid", "type": {"type": "fixed", "namespace": "Energistics.Etp.v12.Datatypes", "name": "Uuid", "size": 16, "fullName": "Energistics.Etp.v12.Datatypes.Uuid", "depends": []}}, {"name": "changeKind", "type": {"type": "enum", "namespace": "Energistics.Etp.v12.Datatypes.Object", "name": "ObjectChangeKind", "symbols": ["insert", "update", "authorized", "joined", "unjoined", "joinedSubscription", "unjoinedSubscription"], "fullName": "Energistics.Etp.v12.Datatypes.Object.ObjectChangeKind", "depends": []}}, {"name": "changeTime", "type": "long"}, {"name": "format", "type": "string", "default": ""}, {"name": "parts", "type": {"type": "array", "items": {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes.Object", "name": "ObjectPart", "fields": [{"name": "uid", "type": "string"}, {"name": "data", "type": "bytes"}], "fullName": "Energistics.Etp.v12.Datatypes.Object.ObjectPart", "depends": []}}}], "fullName": "Energistics.Etp.v12.Protocol.GrowingObjectNotification.PartsChanged", "depends": ["Energistics.Etp.v12.Datatypes.Uuid", "Energistics.Etp.v12.Datatypes.Object.ObjectChangeKind", "Energistics.Etp.v12.Datatypes.Object.ObjectPart"]}'


class PartsChanged(ETPModel):

    uri: str = Field(alias="uri")

    request_uuid: Uuid = Field(alias="requestUuid")

    change_kind: ObjectChangeKind = Field(alias="changeKind")

    change_time: int = Field(alias="changeTime")

    parts: typing.List[ObjectPart] = Field(alias="parts")

    format_: str = Field(alias="format", default="")
