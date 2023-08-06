# -*- coding: utf-8 -*-

""" avro python class for file: contact """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "Contact", "fields": [{"name": "organizationName", "type": "string", "default": ""}, {"name": "contactName", "type": "string", "default": ""}, {"name": "contactPhone", "type": "string", "default": ""}, {"name": "contactEmail", "type": "string", "default": ""}], "fullName": "Energistics.Etp.v12.Datatypes.Contact", "depends": []}'


class Contact(ETPModel):

    organization_name: str = Field(alias="organizationName", default="")

    contact_name: str = Field(alias="contactName", default="")

    contact_phone: str = Field(alias="contactPhone", default="")

    contact_email: str = Field(alias="contactEmail", default="")
