# -*- coding: utf-8 -*-

""" avro python class for file: chunk """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


from etptypes.energistics.etp.v12.datatypes.uuid import Uuid


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Protocol.Store", "name": "Chunk", "protocol": "4", "messageType": "8", "senderRole": "store,customer", "protocolRoles": "store,customer", "multipartFlag": true, "fields": [{"name": "blobId", "type": {"type": "fixed", "namespace": "Energistics.Etp.v12.Datatypes", "name": "Uuid", "size": 16, "fullName": "Energistics.Etp.v12.Datatypes.Uuid", "depends": []}}, {"name": "data", "type": "bytes"}, {"name": "final", "type": "boolean"}], "fullName": "Energistics.Etp.v12.Protocol.Store.Chunk", "depends": ["Energistics.Etp.v12.Datatypes.Uuid"]}'


class Chunk(ETPModel):

    blob_id: Uuid = Field(alias="blobId")

    data: bytes = Field(alias="data")

    final: bool = Field(alias="final")
