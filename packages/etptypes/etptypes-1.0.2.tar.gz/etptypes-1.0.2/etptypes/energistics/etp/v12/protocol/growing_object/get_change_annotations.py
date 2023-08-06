# -*- coding: utf-8 -*-

""" avro python class for file: get_change_annotations """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Protocol.GrowingObject", "name": "GetChangeAnnotations", "protocol": "6", "messageType": "19", "senderRole": "customer", "protocolRoles": "store,customer", "multipartFlag": false, "fields": [{"name": "sinceChangeTime", "type": "long"}, {"name": "uris", "type": {"type": "map", "values": "string"}}, {"name": "latestOnly", "type": "boolean", "default": false}], "fullName": "Energistics.Etp.v12.Protocol.GrowingObject.GetChangeAnnotations", "depends": []}'


class GetChangeAnnotations(ETPModel):

    since_change_time: int = Field(alias="sinceChangeTime")

    uris: typing.Mapping[str, str] = Field(alias="uris")

    latest_only: bool = Field(alias="latestOnly", default=False)
