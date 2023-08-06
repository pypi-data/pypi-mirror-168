# -*- coding: utf-8 -*-

""" avro python class for file: channel_data_kind """

import typing
from pydantic import validator
from etptypes import StrEnum


avro_schema: typing.Final[
    str
] = '{"type": "enum", "namespace": "Energistics.Etp.v12.Datatypes.ChannelData", "name": "ChannelDataKind", "symbols": ["DateTime", "ElapsedTime", "MeasuredDepth", "PassIndexedDepth", "TrueVerticalDepth", "typeBoolean", "typeInt", "typeLong", "typeFloat", "typeDouble", "typeString", "typeBytes"], "fullName": "Energistics.Etp.v12.Datatypes.ChannelData.ChannelDataKind", "depends": []}'


class ChannelDataKind(StrEnum):
    DATE_TIME = "DateTime"
    ELAPSED_TIME = "ElapsedTime"
    MEASURED_DEPTH = "MeasuredDepth"
    PASS_INDEXED_DEPTH = "PassIndexedDepth"
    TRUE_VERTICAL_DEPTH = "TrueVerticalDepth"
    TYPE_BOOLEAN = "typeBoolean"
    TYPE_INT = "typeInt"
    TYPE_LONG = "typeLong"
    TYPE_FLOAT = "typeFloat"
    TYPE_DOUBLE = "typeDouble"
    TYPE_STRING = "typeString"
    TYPE_BYTES = "typeBytes"
