# -*- coding: utf-8 -*-

""" avro python class for file: put_growing_data_objects_header_response """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Protocol.GrowingObject", "name": "PutGrowingDataObjectsHeaderResponse", "protocol": "6", "messageType": "17", "senderRole": "store", "protocolRoles": "store,customer", "multipartFlag": true, "fields": [{"name": "success", "type": {"type": "map", "values": "string"}}], "fullName": "Energistics.Etp.v12.Protocol.GrowingObject.PutGrowingDataObjectsHeaderResponse", "depends": []}'


class PutGrowingDataObjectsHeaderResponse(ETPModel):

    success: typing.Mapping[str, str] = Field(alias="success")
