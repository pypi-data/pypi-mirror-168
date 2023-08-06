# -*- coding: utf-8 -*-

""" avro python class for file: subscribe_part_notifications_response """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Protocol.GrowingObjectNotification", "name": "SubscribePartNotificationsResponse", "protocol": "7", "messageType": "10", "senderRole": "store", "protocolRoles": "store,customer", "multipartFlag": true, "fields": [{"name": "success", "type": {"type": "map", "values": "string"}}], "fullName": "Energistics.Etp.v12.Protocol.GrowingObjectNotification.SubscribePartNotificationsResponse", "depends": []}'


class SubscribePartNotificationsResponse(ETPModel):

    success: typing.Mapping[str, str] = Field(alias="success")
