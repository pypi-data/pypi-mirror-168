# -*- coding: utf-8 -*-

""" avro python class for file: context_info """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


from etptypes.energistics.etp.v12.datatypes.object.relationship_kind import (
    RelationshipKind,
)


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Datatypes.Object", "name": "ContextInfo", "fields": [{"name": "uri", "type": "string"}, {"name": "depth", "type": "int"}, {"name": "dataObjectTypes", "type": {"type": "array", "items": "string"}, "default": []}, {"name": "navigableEdges", "type": {"type": "enum", "namespace": "Energistics.Etp.v12.Datatypes.Object", "name": "RelationshipKind", "symbols": ["Primary", "Secondary", "Both"], "fullName": "Energistics.Etp.v12.Datatypes.Object.RelationshipKind", "depends": []}}, {"name": "includeSecondaryTargets", "type": "boolean", "default": false}, {"name": "includeSecondarySources", "type": "boolean", "default": false}], "fullName": "Energistics.Etp.v12.Datatypes.Object.ContextInfo", "depends": ["Energistics.Etp.v12.Datatypes.Object.RelationshipKind"]}'


class ContextInfo(ETPModel):

    uri: str = Field(alias="uri")

    depth: int = Field(alias="depth")

    navigable_edges: RelationshipKind = Field(alias="navigableEdges")

    data_object_types: typing.List[Strict[str]] = Field(
        alias="dataObjectTypes", default_factory=lambda: []
    )

    include_secondary_targets: bool = Field(
        alias="includeSecondaryTargets", default=False
    )

    include_secondary_sources: bool = Field(
        alias="includeSecondarySources", default=False
    )
