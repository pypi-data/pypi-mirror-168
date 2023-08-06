# -*- coding: utf-8 -*-

""" avro python class for file: replace_parts_by_range_response """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Protocol.GrowingObject", "name": "ReplacePartsByRangeResponse", "protocol": "6", "messageType": "18", "senderRole": "store", "protocolRoles": "store,customer", "multipartFlag": false, "fields": [], "fullName": "Energistics.Etp.v12.Protocol.GrowingObject.ReplacePartsByRangeResponse", "depends": []}'


class ReplacePartsByRangeResponse(ETPModel):
    pass
