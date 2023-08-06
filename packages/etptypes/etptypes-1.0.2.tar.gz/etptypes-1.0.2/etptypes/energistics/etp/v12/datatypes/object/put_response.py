# -*- coding: utf-8 -*-

""" avro python class for file: put_response """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Datatypes.Object", "name": "PutResponse", "fields": [{"name": "createdContainedObjectUris", "type": {"type": "array", "items": "string"}, "default": []}, {"name": "deletedContainedObjectUris", "type": {"type": "array", "items": "string"}, "default": []}, {"name": "joinedContainedObjectUris", "type": {"type": "array", "items": "string"}, "default": []}, {"name": "unjoinedContainedObjectUris", "type": {"type": "array", "items": "string"}, "default": []}], "fullName": "Energistics.Etp.v12.Datatypes.Object.PutResponse", "depends": []}'


class PutResponse(ETPModel):

    created_contained_object_uris: typing.List[Strict[str]] = Field(
        alias="createdContainedObjectUris", default_factory=lambda: []
    )

    deleted_contained_object_uris: typing.List[Strict[str]] = Field(
        alias="deletedContainedObjectUris", default_factory=lambda: []
    )

    joined_contained_object_uris: typing.List[Strict[str]] = Field(
        alias="joinedContainedObjectUris", default_factory=lambda: []
    )

    unjoined_contained_object_uris: typing.List[Strict[str]] = Field(
        alias="unjoinedContainedObjectUris", default_factory=lambda: []
    )
