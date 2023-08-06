# -*- coding: utf-8 -*-

""" avro python class for file: attribute_metadata_record """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


from etptypes.energistics.etp.v12.datatypes.channel_data.channel_data_kind import (
    ChannelDataKind,
)


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "AttributeMetadataRecord", "fields": [{"name": "attributeId", "type": "int"}, {"name": "attributeName", "type": "string"}, {"name": "dataKind", "type": {"type": "enum", "namespace": "Energistics.Etp.v12.Datatypes.ChannelData", "name": "ChannelDataKind", "symbols": ["DateTime", "ElapsedTime", "MeasuredDepth", "PassIndexedDepth", "TrueVerticalDepth", "typeBoolean", "typeInt", "typeLong", "typeFloat", "typeDouble", "typeString", "typeBytes"], "fullName": "Energistics.Etp.v12.Datatypes.ChannelData.ChannelDataKind", "depends": []}}, {"name": "uom", "type": "string"}, {"name": "depthDatum", "type": "string"}, {"name": "attributePropertyKindUri", "type": "string"}, {"name": "axisVectorLengths", "type": {"type": "array", "items": "int"}}], "fullName": "Energistics.Etp.v12.Datatypes.AttributeMetadataRecord", "depends": ["Energistics.Etp.v12.Datatypes.ChannelData.ChannelDataKind"]}'


class AttributeMetadataRecord(ETPModel):

    attribute_id: int = Field(alias="attributeId")

    attribute_name: str = Field(alias="attributeName")

    data_kind: ChannelDataKind = Field(alias="dataKind")

    uom: str = Field(alias="uom")

    depth_datum: str = Field(alias="depthDatum")

    attribute_property_kind_uri: str = Field(alias="attributePropertyKindUri")

    axis_vector_lengths: typing.List[Strict[int]] = Field(alias="axisVectorLengths")
