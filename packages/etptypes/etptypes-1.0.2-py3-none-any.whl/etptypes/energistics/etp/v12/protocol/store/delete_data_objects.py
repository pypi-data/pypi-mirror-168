# -*- coding: utf-8 -*-

""" avro python class for file: delete_data_objects """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Protocol.Store", "name": "DeleteDataObjects", "protocol": "4", "messageType": "3", "senderRole": "customer", "protocolRoles": "store,customer", "multipartFlag": false, "fields": [{"name": "uris", "type": {"type": "map", "values": "string"}}, {"name": "pruneContainedObjects", "type": "boolean", "default": false}], "fullName": "Energistics.Etp.v12.Protocol.Store.DeleteDataObjects", "depends": []}'


class DeleteDataObjects(ETPModel):

    uris: typing.Mapping[str, str] = Field(alias="uris")

    prune_contained_objects: bool = Field(alias="pruneContainedObjects", default=False)
