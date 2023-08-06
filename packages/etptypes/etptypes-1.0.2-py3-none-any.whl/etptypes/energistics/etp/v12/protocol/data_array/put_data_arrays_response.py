# -*- coding: utf-8 -*-

""" avro python class for file: put_data_arrays_response """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Protocol.DataArray", "name": "PutDataArraysResponse", "protocol": "9", "messageType": "10", "senderRole": "store", "protocolRoles": "store,customer", "multipartFlag": true, "fields": [{"name": "success", "type": {"type": "map", "values": "string"}}], "fullName": "Energistics.Etp.v12.Protocol.DataArray.PutDataArraysResponse", "depends": []}'


class PutDataArraysResponse(ETPModel):

    success: typing.Mapping[str, str] = Field(alias="success")
