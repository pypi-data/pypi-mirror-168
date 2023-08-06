# -*- coding: utf-8 -*-

""" avro python class for file: pass_direction """

import typing
from pydantic import validator
from etptypes import StrEnum


avro_schema: typing.Final[
    str
] = '{"type": "enum", "namespace": "Energistics.Etp.v12.Datatypes.ChannelData", "name": "PassDirection", "symbols": ["Up", "HoldingSteady", "Down"], "fullName": "Energistics.Etp.v12.Datatypes.ChannelData.PassDirection", "depends": []}'


class PassDirection(StrEnum):
    UP = "Up"
    HOLDING_STEADY = "HoldingSteady"
    DOWN = "Down"
