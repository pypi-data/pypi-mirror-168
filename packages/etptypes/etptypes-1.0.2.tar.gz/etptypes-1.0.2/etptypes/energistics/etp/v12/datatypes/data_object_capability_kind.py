# -*- coding: utf-8 -*-

""" avro python class for file: data_object_capability_kind """

import typing
from pydantic import validator
from etptypes import StrEnum


avro_schema: typing.Final[
    str
] = '{"type": "enum", "namespace": "Energistics.Etp.v12.Datatypes", "name": "DataObjectCapabilityKind", "symbols": ["ActiveTimeoutPeriod", "MaxContainedDataObjectCount", "MaxDataObjectSize", "OrphanedChildrenPrunedOnDelete", "SupportsGet", "SupportsPut", "SupportsDelete", "MaxSecondaryIndexCount"], "fullName": "Energistics.Etp.v12.Datatypes.DataObjectCapabilityKind", "depends": []}'


class DataObjectCapabilityKind(StrEnum):
    ACTIVE_TIMEOUT_PERIOD = "ActiveTimeoutPeriod"
    MAX_CONTAINED_DATA_OBJECT_COUNT = "MaxContainedDataObjectCount"
    MAX_DATA_OBJECT_SIZE = "MaxDataObjectSize"
    ORPHANED_CHILDREN_PRUNED_ON_DELETE = "OrphanedChildrenPrunedOnDelete"
    SUPPORTS_GET = "SupportsGet"
    SUPPORTS_PUT = "SupportsPut"
    SUPPORTS_DELETE = "SupportsDelete"
    MAX_SECONDARY_INDEX_COUNT = "MaxSecondaryIndexCount"
