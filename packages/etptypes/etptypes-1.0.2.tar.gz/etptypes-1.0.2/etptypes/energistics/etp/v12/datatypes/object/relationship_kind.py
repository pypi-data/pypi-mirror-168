# -*- coding: utf-8 -*-

""" avro python class for file: relationship_kind """

import typing
from pydantic import validator
from etptypes import StrEnum


avro_schema: typing.Final[
    str
] = '{"type": "enum", "namespace": "Energistics.Etp.v12.Datatypes.Object", "name": "RelationshipKind", "symbols": ["Primary", "Secondary", "Both"], "fullName": "Energistics.Etp.v12.Datatypes.Object.RelationshipKind", "depends": []}'


class RelationshipKind(StrEnum):
    PRIMARY = "Primary"
    SECONDARY = "Secondary"
    BOTH = "Both"
