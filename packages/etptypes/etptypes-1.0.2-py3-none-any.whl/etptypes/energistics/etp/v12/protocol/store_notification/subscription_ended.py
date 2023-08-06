# -*- coding: utf-8 -*-

""" avro python class for file: subscription_ended """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


from etptypes.energistics.etp.v12.datatypes.uuid import Uuid


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Protocol.StoreNotification", "name": "SubscriptionEnded", "protocol": "5", "messageType": "7", "senderRole": "store", "protocolRoles": "store,customer", "multipartFlag": false, "fields": [{"name": "reason", "type": "string"}, {"name": "requestUuid", "type": {"type": "fixed", "namespace": "Energistics.Etp.v12.Datatypes", "name": "Uuid", "size": 16, "fullName": "Energistics.Etp.v12.Datatypes.Uuid", "depends": []}}], "fullName": "Energistics.Etp.v12.Protocol.StoreNotification.SubscriptionEnded", "depends": ["Energistics.Etp.v12.Datatypes.Uuid"]}'


class SubscriptionEnded(ETPModel):

    reason: str = Field(alias="reason")

    request_uuid: Uuid = Field(alias="requestUuid")
