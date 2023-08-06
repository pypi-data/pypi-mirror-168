# -*- coding: utf-8 -*-

""" avro python class for file: index_direction """

import typing
from pydantic import validator
from etptypes import StrEnum


avro_schema: typing.Final[
    str
] = '{"type": "enum", "namespace": "Energistics.Etp.v12.Datatypes.ChannelData", "name": "IndexDirection", "symbols": ["Increasing", "Decreasing", "Unordered"], "fullName": "Energistics.Etp.v12.Datatypes.ChannelData.IndexDirection", "depends": []}'


class IndexDirection(StrEnum):
    INCREASING = "Increasing"
    DECREASING = "Decreasing"
    UNORDERED = "Unordered"
