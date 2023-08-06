# -*- coding: utf-8 -*-

""" avro python class for file: put_parts_response """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Protocol.GrowingObject", "name": "PutPartsResponse", "protocol": "6", "messageType": "13", "senderRole": "store", "protocolRoles": "store,customer", "multipartFlag": true, "fields": [{"name": "success", "type": {"type": "map", "values": "string"}}], "fullName": "Energistics.Etp.v12.Protocol.GrowingObject.PutPartsResponse", "depends": []}'


class PutPartsResponse(ETPModel):

    success: typing.Mapping[str, str] = Field(alias="success")
