# -*- coding: utf-8 -*-

""" avro python class for file: wmls_delete_from_store_response """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.PrivateProtocols.WitsmlSoap", "name": "WMLS_DeleteFromStoreResponse", "protocol": "2100", "messageType": "4", "senderRole": "store", "protocolRoles": "store,customer", "multipartFlag": false, "fields": [{"name": "Result", "type": "int"}, {"name": "SuppMsgOut", "type": "string"}], "fullName": "Energistics.Etp.v12.PrivateProtocols.WitsmlSoap.WMLS_DeleteFromStoreResponse", "depends": []}'


class WMLS_DeleteFromStoreResponse(ETPModel):

    result: int = Field(alias="Result")

    supp_msg_out: str = Field(alias="SuppMsgOut")
