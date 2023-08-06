# -*- coding: utf-8 -*-

""" avro python class for file: wmls_add_to_store_response """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.PrivateProtocols.WitsmlSoap", "name": "WMLS_AddToStoreResponse", "protocol": "2100", "messageType": "2", "senderRole": "store", "protocolRoles": "store,customer", "multipartFlag": false, "fields": [{"name": "Result", "type": "int"}, {"name": "SuppMsgOut", "type": "string"}], "fullName": "Energistics.Etp.v12.PrivateProtocols.WitsmlSoap.WMLS_AddToStoreResponse", "depends": []}'


class WMLS_AddToStoreResponse(ETPModel):

    result: int = Field(alias="Result")

    supp_msg_out: str = Field(alias="SuppMsgOut")
