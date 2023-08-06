# -*- coding: utf-8 -*-

""" avro python class for file: message_header """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "MessageHeader", "fields": [{"name": "protocol", "type": "int"}, {"name": "messageType", "type": "int"}, {"name": "correlationId", "type": "long"}, {"name": "messageId", "type": "long"}, {"name": "messageFlags", "type": "int"}], "fullName": "Energistics.Etp.v12.Datatypes.MessageHeader", "depends": []}'


class MessageHeader(ETPModel):

    protocol: int = Field(alias="protocol")

    message_type: int = Field(alias="messageType")

    correlation_id: int = Field(alias="correlationId")

    message_id: int = Field(alias="messageId")

    message_flags: int = Field(alias="messageFlags")
