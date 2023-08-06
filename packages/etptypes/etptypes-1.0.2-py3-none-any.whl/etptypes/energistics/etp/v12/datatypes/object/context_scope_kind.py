# -*- coding: utf-8 -*-

""" avro python class for file: context_scope_kind """

import typing
from pydantic import validator
from etptypes import StrEnum


avro_schema: typing.Final[
    str
] = '{"type": "enum", "namespace": "Energistics.Etp.v12.Datatypes.Object", "name": "ContextScopeKind", "symbols": ["self", "sources", "targets", "sourcesOrSelf", "targetsOrSelf"], "fullName": "Energistics.Etp.v12.Datatypes.Object.ContextScopeKind", "depends": []}'


class ContextScopeKind(StrEnum):
    SELF = "self"
    SOURCES = "sources"
    TARGETS = "targets"
    SOURCES_OR_SELF = "sourcesOrSelf"
    TARGETS_OR_SELF = "targetsOrSelf"
