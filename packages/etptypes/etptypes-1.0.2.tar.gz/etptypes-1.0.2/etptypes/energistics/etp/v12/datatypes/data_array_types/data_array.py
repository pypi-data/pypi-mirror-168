# -*- coding: utf-8 -*-

""" avro python class for file: data_array """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


from etptypes.energistics.etp.v12.datatypes.any_array import AnyArray


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Datatypes.DataArrayTypes", "name": "DataArray", "fields": [{"name": "dimensions", "type": {"type": "array", "items": "long"}}, {"name": "data", "type": {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "AnyArray", "fields": [{"name": "item", "type": [{"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "ArrayOfBoolean", "fields": [{"name": "values", "type": {"type": "array", "items": "boolean"}}], "fullName": "Energistics.Etp.v12.Datatypes.ArrayOfBoolean", "depends": []}, {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "ArrayOfInt", "fields": [{"name": "values", "type": {"type": "array", "items": "int"}}], "fullName": "Energistics.Etp.v12.Datatypes.ArrayOfInt", "depends": []}, {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "ArrayOfLong", "fields": [{"name": "values", "type": {"type": "array", "items": "long"}}], "fullName": "Energistics.Etp.v12.Datatypes.ArrayOfLong", "depends": []}, {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "ArrayOfFloat", "fields": [{"name": "values", "type": {"type": "array", "items": "float"}}], "fullName": "Energistics.Etp.v12.Datatypes.ArrayOfFloat", "depends": []}, {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "ArrayOfDouble", "fields": [{"name": "values", "type": {"type": "array", "items": "double"}}], "fullName": "Energistics.Etp.v12.Datatypes.ArrayOfDouble", "depends": []}, {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "ArrayOfString", "fields": [{"name": "values", "type": {"type": "array", "items": "string"}}], "fullName": "Energistics.Etp.v12.Datatypes.ArrayOfString", "depends": []}, "bytes"]}], "fullName": "Energistics.Etp.v12.Datatypes.AnyArray", "depends": ["Energistics.Etp.v12.Datatypes.ArrayOfBoolean", "Energistics.Etp.v12.Datatypes.ArrayOfInt", "Energistics.Etp.v12.Datatypes.ArrayOfLong", "Energistics.Etp.v12.Datatypes.ArrayOfFloat", "Energistics.Etp.v12.Datatypes.ArrayOfDouble", "Energistics.Etp.v12.Datatypes.ArrayOfString"]}}], "fullName": "Energistics.Etp.v12.Datatypes.DataArrayTypes.DataArray", "depends": ["Energistics.Etp.v12.Datatypes.AnyArray"]}'


class DataArray(ETPModel):

    dimensions: typing.List[Strict[int]] = Field(alias="dimensions")

    data: AnyArray = Field(alias="data")
