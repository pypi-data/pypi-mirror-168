# -*- coding: utf-8 -*-

""" avro python class for file: supported_type """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


from etptypes.energistics.etp.v12.datatypes.object.relationship_kind import (
    RelationshipKind,
)


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Datatypes.Object", "name": "SupportedType", "fields": [{"name": "dataObjectType", "type": "string"}, {"name": "objectCount", "type": ["null", "int"]}, {"name": "relationshipKind", "type": {"type": "enum", "namespace": "Energistics.Etp.v12.Datatypes.Object", "name": "RelationshipKind", "symbols": ["Primary", "Secondary", "Both"], "fullName": "Energistics.Etp.v12.Datatypes.Object.RelationshipKind", "depends": []}}], "fullName": "Energistics.Etp.v12.Datatypes.Object.SupportedType", "depends": ["Energistics.Etp.v12.Datatypes.Object.RelationshipKind"]}'


class SupportedType(ETPModel):

    data_object_type: str = Field(alias="dataObjectType")

    object_count: typing.Optional[Strict[int]] = Field(alias="objectCount")

    relationship_kind: RelationshipKind = Field(alias="relationshipKind")
