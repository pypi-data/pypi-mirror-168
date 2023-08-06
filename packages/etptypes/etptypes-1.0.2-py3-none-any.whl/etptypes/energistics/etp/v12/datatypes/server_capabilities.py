# -*- coding: utf-8 -*-

""" avro python class for file: server_capabilities """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


from etptypes.energistics.etp.v12.datatypes.contact import Contact

from etptypes.energistics.etp.v12.datatypes.supported_data_object import (
    SupportedDataObject,
)

from etptypes.energistics.etp.v12.datatypes.supported_protocol import SupportedProtocol

from etptypes.energistics.etp.v12.datatypes.data_value import DataValue


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "ServerCapabilities", "fields": [{"name": "applicationName", "type": "string"}, {"name": "applicationVersion", "type": "string"}, {"name": "contactInformation", "type": {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "Contact", "fields": [{"name": "organizationName", "type": "string", "default": ""}, {"name": "contactName", "type": "string", "default": ""}, {"name": "contactPhone", "type": "string", "default": ""}, {"name": "contactEmail", "type": "string", "default": ""}], "fullName": "Energistics.Etp.v12.Datatypes.Contact", "depends": []}}, {"name": "supportedCompression", "type": {"type": "array", "items": "string"}, "default": []}, {"name": "supportedEncodings", "type": {"type": "array", "items": "string"}, "default": ["binary"]}, {"name": "supportedFormats", "type": {"type": "array", "items": "string"}, "default": ["xml"]}, {"name": "supportedDataObjects", "type": {"type": "array", "items": {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "SupportedDataObject", "fields": [{"name": "qualifiedType", "type": "string"}, {"name": "dataObjectCapabilities", "type": {"type": "map", "values": {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "DataValue", "fields": [{"name": "item", "type": ["null", "boolean", "int", "long", "float", "double", "string", {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "ArrayOfBoolean", "fields": [{"name": "values", "type": {"type": "array", "items": "boolean"}}], "fullName": "Energistics.Etp.v12.Datatypes.ArrayOfBoolean", "depends": []}, {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "ArrayOfNullableBoolean", "fields": [{"name": "values", "type": {"type": "array", "items": ["null", "boolean"]}}], "fullName": "Energistics.Etp.v12.Datatypes.ArrayOfNullableBoolean", "depends": []}, {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "ArrayOfInt", "fields": [{"name": "values", "type": {"type": "array", "items": "int"}}], "fullName": "Energistics.Etp.v12.Datatypes.ArrayOfInt", "depends": []}, {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "ArrayOfNullableInt", "fields": [{"name": "values", "type": {"type": "array", "items": ["null", "int"]}}], "fullName": "Energistics.Etp.v12.Datatypes.ArrayOfNullableInt", "depends": []}, {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "ArrayOfLong", "fields": [{"name": "values", "type": {"type": "array", "items": "long"}}], "fullName": "Energistics.Etp.v12.Datatypes.ArrayOfLong", "depends": []}, {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "ArrayOfNullableLong", "fields": [{"name": "values", "type": {"type": "array", "items": ["null", "long"]}}], "fullName": "Energistics.Etp.v12.Datatypes.ArrayOfNullableLong", "depends": []}, {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "ArrayOfFloat", "fields": [{"name": "values", "type": {"type": "array", "items": "float"}}], "fullName": "Energistics.Etp.v12.Datatypes.ArrayOfFloat", "depends": []}, {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "ArrayOfDouble", "fields": [{"name": "values", "type": {"type": "array", "items": "double"}}], "fullName": "Energistics.Etp.v12.Datatypes.ArrayOfDouble", "depends": []}, {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "ArrayOfString", "fields": [{"name": "values", "type": {"type": "array", "items": "string"}}], "fullName": "Energistics.Etp.v12.Datatypes.ArrayOfString", "depends": []}, {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "ArrayOfBytes", "fields": [{"name": "values", "type": {"type": "array", "items": "bytes"}}], "fullName": "Energistics.Etp.v12.Datatypes.ArrayOfBytes", "depends": []}, "bytes", {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "AnySparseArray", "fields": [{"name": "slices", "type": {"type": "array", "items": {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "AnySubarray", "fields": [{"name": "start", "type": "long"}, {"name": "slice", "type": {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "AnyArray", "fields": [{"name": "item", "type": ["Energistics.Etp.v12.Datatypes.ArrayOfBoolean", "Energistics.Etp.v12.Datatypes.ArrayOfInt", "Energistics.Etp.v12.Datatypes.ArrayOfLong", "Energistics.Etp.v12.Datatypes.ArrayOfFloat", "Energistics.Etp.v12.Datatypes.ArrayOfDouble", "Energistics.Etp.v12.Datatypes.ArrayOfString", "bytes"]}], "fullName": "Energistics.Etp.v12.Datatypes.AnyArray", "depends": ["Energistics.Etp.v12.Datatypes.ArrayOfBoolean", "Energistics.Etp.v12.Datatypes.ArrayOfInt", "Energistics.Etp.v12.Datatypes.ArrayOfLong", "Energistics.Etp.v12.Datatypes.ArrayOfFloat", "Energistics.Etp.v12.Datatypes.ArrayOfDouble", "Energistics.Etp.v12.Datatypes.ArrayOfString"]}}], "fullName": "Energistics.Etp.v12.Datatypes.AnySubarray", "depends": ["Energistics.Etp.v12.Datatypes.AnyArray"]}}}], "fullName": "Energistics.Etp.v12.Datatypes.AnySparseArray", "depends": ["Energistics.Etp.v12.Datatypes.AnySubarray"]}]}], "fullName": "Energistics.Etp.v12.Datatypes.DataValue", "depends": ["Energistics.Etp.v12.Datatypes.ArrayOfBoolean", "Energistics.Etp.v12.Datatypes.ArrayOfNullableBoolean", "Energistics.Etp.v12.Datatypes.ArrayOfInt", "Energistics.Etp.v12.Datatypes.ArrayOfNullableInt", "Energistics.Etp.v12.Datatypes.ArrayOfLong", "Energistics.Etp.v12.Datatypes.ArrayOfNullableLong", "Energistics.Etp.v12.Datatypes.ArrayOfFloat", "Energistics.Etp.v12.Datatypes.ArrayOfDouble", "Energistics.Etp.v12.Datatypes.ArrayOfString", "Energistics.Etp.v12.Datatypes.ArrayOfBytes", "Energistics.Etp.v12.Datatypes.AnySparseArray"]}}, "default": {}}], "fullName": "Energistics.Etp.v12.Datatypes.SupportedDataObject", "depends": ["Energistics.Etp.v12.Datatypes.DataValue"]}}}, {"name": "supportedProtocols", "type": {"type": "array", "items": {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "SupportedProtocol", "fields": [{"name": "protocol", "type": "int"}, {"name": "protocolVersion", "type": {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "Version", "fields": [{"name": "major", "type": "int", "default": 0}, {"name": "minor", "type": "int", "default": 0}, {"name": "revision", "type": "int", "default": 0}, {"name": "patch", "type": "int", "default": 0}], "fullName": "Energistics.Etp.v12.Datatypes.Version", "depends": []}}, {"name": "role", "type": "string"}, {"name": "protocolCapabilities", "type": {"type": "map", "values": "Energistics.Etp.v12.Datatypes.DataValue"}, "default": {}}], "fullName": "Energistics.Etp.v12.Datatypes.SupportedProtocol", "depends": ["Energistics.Etp.v12.Datatypes.Version", "Energistics.Etp.v12.Datatypes.DataValue"]}}}, {"name": "endpointCapabilities", "type": {"type": "map", "values": "Energistics.Etp.v12.Datatypes.DataValue"}, "default": {}}], "fullName": "Energistics.Etp.v12.Datatypes.ServerCapabilities", "depends": ["Energistics.Etp.v12.Datatypes.Contact", "Energistics.Etp.v12.Datatypes.SupportedDataObject", "Energistics.Etp.v12.Datatypes.SupportedProtocol", "Energistics.Etp.v12.Datatypes.DataValue"]}'


class ServerCapabilities(ETPModel):

    application_name: str = Field(alias="applicationName")

    application_version: str = Field(alias="applicationVersion")

    contact_information: Contact = Field(alias="contactInformation")

    supported_data_objects: typing.List[SupportedDataObject] = Field(
        alias="supportedDataObjects"
    )

    supported_protocols: typing.List[SupportedProtocol] = Field(
        alias="supportedProtocols"
    )

    supported_compression: typing.List[Strict[str]] = Field(
        alias="supportedCompression", default_factory=lambda: []
    )

    supported_encodings: typing.List[Strict[str]] = Field(
        alias="supportedEncodings", default_factory=lambda: ["binary"]
    )

    supported_formats: typing.List[Strict[str]] = Field(
        alias="supportedFormats", default_factory=lambda: ["xml"]
    )

    endpoint_capabilities: typing.Mapping[str, DataValue] = Field(
        alias="endpointCapabilities", default_factory=lambda: {}
    )
