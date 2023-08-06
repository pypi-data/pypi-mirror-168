# -*- coding: utf-8 -*-

""" avro python class for file: get_dataspaces """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Protocol.Dataspace", "name": "GetDataspaces", "protocol": "24", "messageType": "1", "senderRole": "customer", "protocolRoles": "store,customer", "multipartFlag": false, "fields": [{"name": "storeLastWriteFilter", "type": ["null", "long"]}], "fullName": "Energistics.Etp.v12.Protocol.Dataspace.GetDataspaces", "depends": []}'


class GetDataspaces(ETPModel):

    store_last_write_filter: typing.Optional[Strict[int]] = Field(
        alias="storeLastWriteFilter"
    )
