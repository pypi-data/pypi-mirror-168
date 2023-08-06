# -*- coding: utf-8 -*-

""" avro python class for file: get_data_subarrays_type """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


from etptypes.energistics.etp.v12.datatypes.data_array_types.data_array_identifier import (
    DataArrayIdentifier,
)


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Datatypes.DataArrayTypes", "name": "GetDataSubarraysType", "fields": [{"name": "uid", "type": {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes.DataArrayTypes", "name": "DataArrayIdentifier", "fields": [{"name": "uri", "type": "string"}, {"name": "pathInResource", "type": "string"}], "fullName": "Energistics.Etp.v12.Datatypes.DataArrayTypes.DataArrayIdentifier", "depends": []}}, {"name": "starts", "type": {"type": "array", "items": "long"}, "default": []}, {"name": "counts", "type": {"type": "array", "items": "long"}, "default": []}], "fullName": "Energistics.Etp.v12.Datatypes.DataArrayTypes.GetDataSubarraysType", "depends": ["Energistics.Etp.v12.Datatypes.DataArrayTypes.DataArrayIdentifier"]}'


class GetDataSubarraysType(ETPModel):

    uid: DataArrayIdentifier = Field(alias="uid")

    starts: typing.List[Strict[int]] = Field(alias="starts", default_factory=lambda: [])

    counts: typing.List[Strict[int]] = Field(alias="counts", default_factory=lambda: [])
