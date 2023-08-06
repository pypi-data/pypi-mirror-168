# -*- coding: utf-8 -*-

""" avro python class for file: put_dataspaces_response """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Protocol.Dataspace", "name": "PutDataspacesResponse", "protocol": "24", "messageType": "6", "senderRole": "store", "protocolRoles": "store,customer", "multipartFlag": true, "fields": [{"name": "success", "type": {"type": "map", "values": "string"}}], "fullName": "Energistics.Etp.v12.Protocol.Dataspace.PutDataspacesResponse", "depends": []}'


class PutDataspacesResponse(ETPModel):

    success: typing.Mapping[str, str] = Field(alias="success")
