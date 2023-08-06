# -*- coding: utf-8 -*-

""" avro python class for file: get_data_subarrays_response """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


from etptypes.energistics.etp.v12.datatypes.data_array_types.data_array import DataArray


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Protocol.DataArray", "name": "GetDataSubarraysResponse", "protocol": "9", "messageType": "8", "senderRole": "store", "protocolRoles": "store,customer", "multipartFlag": true, "fields": [{"name": "dataSubarrays", "type": {"type": "map", "values": {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes.DataArrayTypes", "name": "DataArray", "fields": [{"name": "dimensions", "type": {"type": "array", "items": "long"}}, {"name": "data", "type": {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "AnyArray", "fields": [{"name": "item", "type": [{"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "ArrayOfBoolean", "fields": [{"name": "values", "type": {"type": "array", "items": "boolean"}}], "fullName": "Energistics.Etp.v12.Datatypes.ArrayOfBoolean", "depends": []}, {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "ArrayOfInt", "fields": [{"name": "values", "type": {"type": "array", "items": "int"}}], "fullName": "Energistics.Etp.v12.Datatypes.ArrayOfInt", "depends": []}, {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "ArrayOfLong", "fields": [{"name": "values", "type": {"type": "array", "items": "long"}}], "fullName": "Energistics.Etp.v12.Datatypes.ArrayOfLong", "depends": []}, {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "ArrayOfFloat", "fields": [{"name": "values", "type": {"type": "array", "items": "float"}}], "fullName": "Energistics.Etp.v12.Datatypes.ArrayOfFloat", "depends": []}, {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "ArrayOfDouble", "fields": [{"name": "values", "type": {"type": "array", "items": "double"}}], "fullName": "Energistics.Etp.v12.Datatypes.ArrayOfDouble", "depends": []}, {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "ArrayOfString", "fields": [{"name": "values", "type": {"type": "array", "items": "string"}}], "fullName": "Energistics.Etp.v12.Datatypes.ArrayOfString", "depends": []}, "bytes"]}], "fullName": "Energistics.Etp.v12.Datatypes.AnyArray", "depends": ["Energistics.Etp.v12.Datatypes.ArrayOfBoolean", "Energistics.Etp.v12.Datatypes.ArrayOfInt", "Energistics.Etp.v12.Datatypes.ArrayOfLong", "Energistics.Etp.v12.Datatypes.ArrayOfFloat", "Energistics.Etp.v12.Datatypes.ArrayOfDouble", "Energistics.Etp.v12.Datatypes.ArrayOfString"]}}], "fullName": "Energistics.Etp.v12.Datatypes.DataArrayTypes.DataArray", "depends": ["Energistics.Etp.v12.Datatypes.AnyArray"]}}, "default": {}}], "fullName": "Energistics.Etp.v12.Protocol.DataArray.GetDataSubarraysResponse", "depends": ["Energistics.Etp.v12.Datatypes.DataArrayTypes.DataArray"]}'


class GetDataSubarraysResponse(ETPModel):

    data_subarrays: typing.Mapping[str, DataArray] = Field(
        alias="dataSubarrays", default_factory=lambda: {}
    )
