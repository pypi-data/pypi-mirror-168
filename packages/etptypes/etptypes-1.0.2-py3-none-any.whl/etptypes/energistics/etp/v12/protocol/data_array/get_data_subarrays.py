# -*- coding: utf-8 -*-

""" avro python class for file: get_data_subarrays """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


from etptypes.energistics.etp.v12.datatypes.data_array_types.get_data_subarrays_type import (
    GetDataSubarraysType,
)


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Protocol.DataArray", "name": "GetDataSubarrays", "protocol": "9", "messageType": "3", "senderRole": "customer", "protocolRoles": "store,customer", "multipartFlag": false, "fields": [{"name": "dataSubarrays", "type": {"type": "map", "values": {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes.DataArrayTypes", "name": "GetDataSubarraysType", "fields": [{"name": "uid", "type": {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes.DataArrayTypes", "name": "DataArrayIdentifier", "fields": [{"name": "uri", "type": "string"}, {"name": "pathInResource", "type": "string"}], "fullName": "Energistics.Etp.v12.Datatypes.DataArrayTypes.DataArrayIdentifier", "depends": []}}, {"name": "starts", "type": {"type": "array", "items": "long"}, "default": []}, {"name": "counts", "type": {"type": "array", "items": "long"}, "default": []}], "fullName": "Energistics.Etp.v12.Datatypes.DataArrayTypes.GetDataSubarraysType", "depends": ["Energistics.Etp.v12.Datatypes.DataArrayTypes.DataArrayIdentifier"]}}}], "fullName": "Energistics.Etp.v12.Protocol.DataArray.GetDataSubarrays", "depends": ["Energistics.Etp.v12.Datatypes.DataArrayTypes.GetDataSubarraysType"]}'


class GetDataSubarrays(ETPModel):

    data_subarrays: typing.Mapping[str, GetDataSubarraysType] = Field(
        alias="dataSubarrays"
    )
