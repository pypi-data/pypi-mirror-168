# -*- coding: utf-8 -*-

""" avro python class for file: get_deleted_resources """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Protocol.Discovery", "name": "GetDeletedResources", "protocol": "3", "messageType": "5", "senderRole": "customer", "protocolRoles": "store,customer", "multipartFlag": false, "fields": [{"name": "dataspaceUri", "type": "string"}, {"name": "deleteTimeFilter", "type": ["null", "long"]}, {"name": "dataObjectTypes", "type": {"type": "array", "items": "string"}, "default": []}], "fullName": "Energistics.Etp.v12.Protocol.Discovery.GetDeletedResources", "depends": []}'


class GetDeletedResources(ETPModel):

    dataspace_uri: str = Field(alias="dataspaceUri")

    delete_time_filter: typing.Optional[Strict[int]] = Field(alias="deleteTimeFilter")

    data_object_types: typing.List[Strict[str]] = Field(
        alias="dataObjectTypes", default_factory=lambda: []
    )
