# -*- coding: utf-8 -*-

""" avro python class for file: protocol_exception """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


from etptypes.energistics.etp.v12.datatypes.error_info import ErrorInfo


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Protocol.Core", "name": "ProtocolException", "protocol": "0", "messageType": "1000", "senderRole": "*", "protocolRoles": "client, server", "multipartFlag": true, "fields": [{"name": "error", "type": ["null", {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "ErrorInfo", "fields": [{"name": "message", "type": "string"}, {"name": "code", "type": "int"}], "fullName": "Energistics.Etp.v12.Datatypes.ErrorInfo", "depends": []}]}, {"name": "errors", "type": {"type": "map", "values": "Energistics.Etp.v12.Datatypes.ErrorInfo"}, "default": {}}], "fullName": "Energistics.Etp.v12.Protocol.Core.ProtocolException", "depends": ["Energistics.Etp.v12.Datatypes.ErrorInfo"]}'


class ProtocolException(ETPModel):

    error: typing.Optional[ErrorInfo] = Field(alias="error")

    errors: typing.Mapping[str, ErrorInfo] = Field(
        alias="errors", default_factory=lambda: {}
    )
