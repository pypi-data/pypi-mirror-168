# -*- coding: utf-8 -*-

""" avro python class for file: delete_data_objects_response """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


from etptypes.energistics.etp.v12.datatypes.array_of_string import ArrayOfString


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Protocol.Store", "name": "DeleteDataObjectsResponse", "protocol": "4", "messageType": "10", "senderRole": "store", "protocolRoles": "store,customer", "multipartFlag": true, "fields": [{"name": "deletedUris", "type": {"type": "map", "values": {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "ArrayOfString", "fields": [{"name": "values", "type": {"type": "array", "items": "string"}}], "fullName": "Energistics.Etp.v12.Datatypes.ArrayOfString", "depends": []}}}], "fullName": "Energistics.Etp.v12.Protocol.Store.DeleteDataObjectsResponse", "depends": ["Energistics.Etp.v12.Datatypes.ArrayOfString"]}'


class DeleteDataObjectsResponse(ETPModel):

    deleted_uris: typing.Mapping[str, ArrayOfString] = Field(alias="deletedUris")
