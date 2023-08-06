# -*- coding: utf-8 -*-

""" avro python class for file: delete_dataspaces """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Protocol.Dataspace", "name": "DeleteDataspaces", "protocol": "24", "messageType": "4", "senderRole": "customer", "protocolRoles": "store,customer", "multipartFlag": false, "fields": [{"name": "uris", "type": {"type": "map", "values": "string"}}], "fullName": "Energistics.Etp.v12.Protocol.Dataspace.DeleteDataspaces", "depends": []}'


class DeleteDataspaces(ETPModel):

    uris: typing.Mapping[str, str] = Field(alias="uris")
