# -*- coding: utf-8 -*-

""" avro python class for file: start_transaction """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Protocol.Transaction", "name": "StartTransaction", "protocol": "18", "messageType": "1", "senderRole": "customer", "protocolRoles": "store,customer", "multipartFlag": false, "fields": [{"name": "readOnly", "type": "boolean"}, {"name": "message", "type": "string", "default": ""}, {"name": "dataspaceUris", "type": {"type": "array", "items": "string"}, "default": [""]}], "fullName": "Energistics.Etp.v12.Protocol.Transaction.StartTransaction", "depends": []}'


class StartTransaction(ETPModel):

    read_only: bool = Field(alias="readOnly")

    message: str = Field(alias="message", default="")

    dataspace_uris: typing.List[Strict[str]] = Field(
        alias="dataspaceUris", default_factory=lambda: [""]
    )
