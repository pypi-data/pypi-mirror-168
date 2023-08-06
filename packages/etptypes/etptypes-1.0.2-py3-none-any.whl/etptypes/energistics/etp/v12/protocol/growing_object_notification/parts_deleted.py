# -*- coding: utf-8 -*-

""" avro python class for file: parts_deleted """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


from etptypes.energistics.etp.v12.datatypes.uuid import Uuid


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Protocol.GrowingObjectNotification", "name": "PartsDeleted", "protocol": "7", "messageType": "3", "senderRole": "store", "protocolRoles": "store,customer", "multipartFlag": false, "fields": [{"name": "uri", "type": "string"}, {"name": "requestUuid", "type": {"type": "fixed", "namespace": "Energistics.Etp.v12.Datatypes", "name": "Uuid", "size": 16, "fullName": "Energistics.Etp.v12.Datatypes.Uuid", "depends": []}}, {"name": "changeTime", "type": "long"}, {"name": "uids", "type": {"type": "array", "items": "string"}}], "fullName": "Energistics.Etp.v12.Protocol.GrowingObjectNotification.PartsDeleted", "depends": ["Energistics.Etp.v12.Datatypes.Uuid"]}'


class PartsDeleted(ETPModel):

    uri: str = Field(alias="uri")

    request_uuid: Uuid = Field(alias="requestUuid")

    change_time: int = Field(alias="changeTime")

    uids: typing.List[Strict[str]] = Field(alias="uids")
