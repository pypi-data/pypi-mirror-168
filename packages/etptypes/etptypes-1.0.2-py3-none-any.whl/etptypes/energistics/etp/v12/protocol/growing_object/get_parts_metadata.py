# -*- coding: utf-8 -*-

""" avro python class for file: get_parts_metadata """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Protocol.GrowingObject", "name": "GetPartsMetadata", "protocol": "6", "messageType": "8", "senderRole": "customer", "protocolRoles": "store,customer", "multipartFlag": false, "fields": [{"name": "uris", "type": {"type": "map", "values": "string"}}], "fullName": "Energistics.Etp.v12.Protocol.GrowingObject.GetPartsMetadata", "depends": []}'


class GetPartsMetadata(ETPModel):

    uris: typing.Mapping[str, str] = Field(alias="uris")
