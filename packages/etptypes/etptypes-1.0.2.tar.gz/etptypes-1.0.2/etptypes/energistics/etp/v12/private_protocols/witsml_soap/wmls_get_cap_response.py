# -*- coding: utf-8 -*-

""" avro python class for file: wmls_get_cap_response """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.PrivateProtocols.WitsmlSoap", "name": "WMLS_GetCapResponse", "protocol": "2100", "messageType": "8", "senderRole": "store", "protocolRoles": "store,customer", "multipartFlag": false, "fields": [{"name": "Result", "type": "int"}, {"name": "CapabilitiesOut", "type": "string"}, {"name": "SuppMsgOut", "type": "string"}], "fullName": "Energistics.Etp.v12.PrivateProtocols.WitsmlSoap.WMLS_GetCapResponse", "depends": []}'


class WMLS_GetCapResponse(ETPModel):

    result: int = Field(alias="Result")

    capabilities_out: str = Field(alias="CapabilitiesOut")

    supp_msg_out: str = Field(alias="SuppMsgOut")
