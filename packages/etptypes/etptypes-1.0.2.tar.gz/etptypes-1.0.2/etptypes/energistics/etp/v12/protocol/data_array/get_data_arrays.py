# -*- coding: utf-8 -*-

""" avro python class for file: get_data_arrays """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


from etptypes.energistics.etp.v12.datatypes.data_array_types.data_array_identifier import (
    DataArrayIdentifier,
)


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Protocol.DataArray", "name": "GetDataArrays", "protocol": "9", "messageType": "2", "senderRole": "customer", "protocolRoles": "store,customer", "multipartFlag": false, "fields": [{"name": "dataArrays", "type": {"type": "map", "values": {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes.DataArrayTypes", "name": "DataArrayIdentifier", "fields": [{"name": "uri", "type": "string"}, {"name": "pathInResource", "type": "string"}], "fullName": "Energistics.Etp.v12.Datatypes.DataArrayTypes.DataArrayIdentifier", "depends": []}}}], "fullName": "Energistics.Etp.v12.Protocol.DataArray.GetDataArrays", "depends": ["Energistics.Etp.v12.Datatypes.DataArrayTypes.DataArrayIdentifier"]}'


class GetDataArrays(ETPModel):

    data_arrays: typing.Mapping[str, DataArrayIdentifier] = Field(alias="dataArrays")
