# -*- coding: utf-8 -*-

""" avro python class for file: wmls_get_base_msg_response """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.PrivateProtocols.WitsmlSoap", "name": "WMLS_GetBaseMsgResponse", "protocol": "2100", "messageType": "6", "senderRole": "store", "protocolRoles": "store,customer", "multipartFlag": false, "fields": [{"name": "Result", "type": "string"}], "fullName": "Energistics.Etp.v12.PrivateProtocols.WitsmlSoap.WMLS_GetBaseMsgResponse", "depends": []}'


class WMLS_GetBaseMsgResponse(ETPModel):

    result: str = Field(alias="Result")
