# -*- coding: utf-8 -*-

""" avro python class for file: wmls_add_to_store """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.PrivateProtocols.WitsmlSoap", "name": "WMLS_AddToStore", "protocol": "2100", "messageType": "1", "senderRole": "customer", "protocolRoles": "store,customer", "multipartFlag": false, "fields": [{"name": "WMLtypeIn", "type": "string"}, {"name": "XMLin", "type": "string"}, {"name": "OptionsIn", "type": "string"}, {"name": "CapabilitiesIn", "type": "string"}], "fullName": "Energistics.Etp.v12.PrivateProtocols.WitsmlSoap.WMLS_AddToStore", "depends": []}'


class WMLS_AddToStore(ETPModel):

    wmltype_in: str = Field(alias="WMLtypeIn")

    xmlin: str = Field(alias="XMLin")

    options_in: str = Field(alias="OptionsIn")

    capabilities_in: str = Field(alias="CapabilitiesIn")
