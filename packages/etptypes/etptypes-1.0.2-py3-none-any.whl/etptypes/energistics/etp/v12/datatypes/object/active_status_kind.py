# -*- coding: utf-8 -*-

""" avro python class for file: active_status_kind """

import typing
from pydantic import validator
from etptypes import StrEnum


avro_schema: typing.Final[
    str
] = '{"type": "enum", "namespace": "Energistics.Etp.v12.Datatypes.Object", "name": "ActiveStatusKind", "symbols": ["Active", "Inactive"], "fullName": "Energistics.Etp.v12.Datatypes.Object.ActiveStatusKind", "depends": []}'


class ActiveStatusKind(StrEnum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
