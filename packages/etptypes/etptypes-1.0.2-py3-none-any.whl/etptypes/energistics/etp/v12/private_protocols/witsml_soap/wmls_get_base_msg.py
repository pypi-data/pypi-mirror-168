# -*- coding: utf-8 -*-

""" avro python class for file: wmls_get_base_msg """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.PrivateProtocols.WitsmlSoap", "name": "WMLS_GetBaseMsg", "protocol": "2100", "messageType": "5", "senderRole": "customer", "protocolRoles": "store,customer", "multipartFlag": false, "fields": [{"name": "ReturnValueIn", "type": "int"}], "fullName": "Energistics.Etp.v12.PrivateProtocols.WitsmlSoap.WMLS_GetBaseMsg", "depends": []}'


class WMLS_GetBaseMsg(ETPModel):

    return_value_in: int = Field(alias="ReturnValueIn")
