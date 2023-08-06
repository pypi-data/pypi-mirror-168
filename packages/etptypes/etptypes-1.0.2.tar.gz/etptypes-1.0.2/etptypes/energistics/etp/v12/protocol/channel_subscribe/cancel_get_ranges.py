# -*- coding: utf-8 -*-

""" avro python class for file: cancel_get_ranges """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


from etptypes.energistics.etp.v12.datatypes.uuid import Uuid


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Protocol.ChannelSubscribe", "name": "CancelGetRanges", "protocol": "21", "messageType": "11", "senderRole": "customer", "protocolRoles": "store,customer", "multipartFlag": false, "fields": [{"name": "requestUuid", "type": {"type": "fixed", "namespace": "Energistics.Etp.v12.Datatypes", "name": "Uuid", "size": 16, "fullName": "Energistics.Etp.v12.Datatypes.Uuid", "depends": []}}], "fullName": "Energistics.Etp.v12.Protocol.ChannelSubscribe.CancelGetRanges", "depends": ["Energistics.Etp.v12.Datatypes.Uuid"]}'


class CancelGetRanges(ETPModel):

    request_uuid: Uuid = Field(alias="requestUuid")
