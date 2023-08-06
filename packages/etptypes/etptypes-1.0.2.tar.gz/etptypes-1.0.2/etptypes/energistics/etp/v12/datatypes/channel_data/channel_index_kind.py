# -*- coding: utf-8 -*-

""" avro python class for file: channel_index_kind """

import typing
from pydantic import validator
from etptypes import StrEnum


avro_schema: typing.Final[
    str
] = '{"type": "enum", "namespace": "Energistics.Etp.v12.Datatypes.ChannelData", "name": "ChannelIndexKind", "symbols": ["DateTime", "ElapsedTime", "MeasuredDepth", "TrueVerticalDepth", "PassIndexedDepth", "Pressure", "Temperature", "Scalar"], "fullName": "Energistics.Etp.v12.Datatypes.ChannelData.ChannelIndexKind", "depends": []}'


class ChannelIndexKind(StrEnum):
    DATE_TIME = "DateTime"
    ELAPSED_TIME = "ElapsedTime"
    MEASURED_DEPTH = "MeasuredDepth"
    TRUE_VERTICAL_DEPTH = "TrueVerticalDepth"
    PASS_INDEXED_DEPTH = "PassIndexedDepth"
    PRESSURE = "Pressure"
    TEMPERATURE = "Temperature"
    SCALAR = "Scalar"
