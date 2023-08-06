# -*- coding: utf-8 -*-

""" avro python class for file: subscribe_notifications_response """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Protocol.StoreNotification", "name": "SubscribeNotificationsResponse", "protocol": "5", "messageType": "10", "senderRole": "store", "protocolRoles": "store,customer", "multipartFlag": true, "fields": [{"name": "success", "type": {"type": "map", "values": "string"}}], "fullName": "Energistics.Etp.v12.Protocol.StoreNotification.SubscribeNotificationsResponse", "depends": []}'


class SubscribeNotificationsResponse(ETPModel):

    success: typing.Mapping[str, str] = Field(alias="success")
