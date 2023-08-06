# -*- coding: utf-8 -*-

""" avro python class for file: wmls_get_from_store """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.PrivateProtocols.WitsmlSoap", "name": "WMLS_GetFromStore", "protocol": "2100", "messageType": "9", "senderRole": "customer", "protocolRoles": "store,customer", "multipartFlag": false, "fields": [{"name": "WMLtypeIn", "type": "string"}, {"name": "XMLin", "type": "string"}, {"name": "OptionsIn", "type": "string"}, {"name": "CapabilitiesIn", "type": "string"}], "fullName": "Energistics.Etp.v12.PrivateProtocols.WitsmlSoap.WMLS_GetFromStore", "depends": []}'


class WMLS_GetFromStore(ETPModel):

    wmltype_in: str = Field(alias="WMLtypeIn")

    xmlin: str = Field(alias="XMLin")

    options_in: str = Field(alias="OptionsIn")

    capabilities_in: str = Field(alias="CapabilitiesIn")
