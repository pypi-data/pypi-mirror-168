# -*- coding: utf-8 -*-

""" avro python class for file: put_data_objects_response """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


from etptypes.energistics.etp.v12.datatypes.object.put_response import PutResponse


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Protocol.Store", "name": "PutDataObjectsResponse", "protocol": "4", "messageType": "9", "senderRole": "store", "protocolRoles": "store,customer", "multipartFlag": true, "fields": [{"name": "success", "type": {"type": "map", "values": {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes.Object", "name": "PutResponse", "fields": [{"name": "createdContainedObjectUris", "type": {"type": "array", "items": "string"}, "default": []}, {"name": "deletedContainedObjectUris", "type": {"type": "array", "items": "string"}, "default": []}, {"name": "joinedContainedObjectUris", "type": {"type": "array", "items": "string"}, "default": []}, {"name": "unjoinedContainedObjectUris", "type": {"type": "array", "items": "string"}, "default": []}], "fullName": "Energistics.Etp.v12.Datatypes.Object.PutResponse", "depends": []}}}], "fullName": "Energistics.Etp.v12.Protocol.Store.PutDataObjectsResponse", "depends": ["Energistics.Etp.v12.Datatypes.Object.PutResponse"]}'


class PutDataObjectsResponse(ETPModel):

    success: typing.Mapping[str, PutResponse] = Field(alias="success")
