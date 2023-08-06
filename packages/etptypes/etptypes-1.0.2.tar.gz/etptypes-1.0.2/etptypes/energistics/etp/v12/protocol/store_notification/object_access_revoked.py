# -*- coding: utf-8 -*-

""" avro python class for file: object_access_revoked """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


from etptypes.energistics.etp.v12.datatypes.uuid import Uuid


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Protocol.StoreNotification", "name": "ObjectAccessRevoked", "protocol": "5", "messageType": "5", "senderRole": "store", "protocolRoles": "store,customer", "multipartFlag": false, "fields": [{"name": "uri", "type": "string"}, {"name": "changeTime", "type": "long"}, {"name": "requestUuid", "type": {"type": "fixed", "namespace": "Energistics.Etp.v12.Datatypes", "name": "Uuid", "size": 16, "fullName": "Energistics.Etp.v12.Datatypes.Uuid", "depends": []}}], "fullName": "Energistics.Etp.v12.Protocol.StoreNotification.ObjectAccessRevoked", "depends": ["Energistics.Etp.v12.Datatypes.Uuid"]}'


class ObjectAccessRevoked(ETPModel):

    uri: str = Field(alias="uri")

    change_time: int = Field(alias="changeTime")

    request_uuid: Uuid = Field(alias="requestUuid")
