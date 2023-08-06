# -*- coding: utf-8 -*-

""" avro python class for file: wmls_get_cap """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.PrivateProtocols.WitsmlSoap", "name": "WMLS_GetCap", "protocol": "2100", "messageType": "7", "senderRole": "customer", "protocolRoles": "store,customer", "multipartFlag": false, "fields": [{"name": "OptionsIn", "type": "string"}], "fullName": "Energistics.Etp.v12.PrivateProtocols.WitsmlSoap.WMLS_GetCap", "depends": []}'


class WMLS_GetCap(ETPModel):

    options_in: str = Field(alias="OptionsIn")
