# -*- coding: utf-8 -*-

""" avro python class for file: delete_parts """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Protocol.GrowingObject", "name": "DeleteParts", "protocol": "6", "messageType": "1", "senderRole": "customer", "protocolRoles": "store,customer", "multipartFlag": false, "fields": [{"name": "uri", "type": "string"}, {"name": "uids", "type": {"type": "map", "values": "string"}}], "fullName": "Energistics.Etp.v12.Protocol.GrowingObject.DeleteParts", "depends": []}'


class DeleteParts(ETPModel):

    uri: str = Field(alias="uri")

    uids: typing.Mapping[str, str] = Field(alias="uids")
