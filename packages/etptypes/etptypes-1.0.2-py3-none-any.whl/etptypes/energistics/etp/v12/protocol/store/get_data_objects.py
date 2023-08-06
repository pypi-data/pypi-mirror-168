# -*- coding: utf-8 -*-

""" avro python class for file: get_data_objects """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Protocol.Store", "name": "GetDataObjects", "protocol": "4", "messageType": "1", "senderRole": "customer", "protocolRoles": "store,customer", "multipartFlag": false, "fields": [{"name": "uris", "type": {"type": "map", "values": "string"}}, {"name": "format", "type": "string", "default": "xml"}], "fullName": "Energistics.Etp.v12.Protocol.Store.GetDataObjects", "depends": []}'


class GetDataObjects(ETPModel):

    uris: typing.Mapping[str, str] = Field(alias="uris")

    format_: str = Field(alias="format", default="xml")
