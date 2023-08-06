# -*- coding: utf-8 -*-

""" avro python class for file: wmls_get_from_store_response """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.PrivateProtocols.WitsmlSoap", "name": "WMLS_GetFromStoreResponse", "protocol": "2100", "messageType": "10", "senderRole": "store", "protocolRoles": "store,customer", "multipartFlag": false, "fields": [{"name": "Result", "type": "int"}, {"name": "XMLout", "type": "string"}, {"name": "SuppMsgOut", "type": "string"}], "fullName": "Energistics.Etp.v12.PrivateProtocols.WitsmlSoap.WMLS_GetFromStoreResponse", "depends": []}'


class WMLS_GetFromStoreResponse(ETPModel):

    result: int = Field(alias="Result")

    xmlout: str = Field(alias="XMLout")

    supp_msg_out: str = Field(alias="SuppMsgOut")
