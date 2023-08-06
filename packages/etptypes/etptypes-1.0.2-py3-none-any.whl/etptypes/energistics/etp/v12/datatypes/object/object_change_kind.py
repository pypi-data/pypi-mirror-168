# -*- coding: utf-8 -*-

""" avro python class for file: object_change_kind """

import typing
from pydantic import validator
from etptypes import StrEnum


avro_schema: typing.Final[
    str
] = '{"type": "enum", "namespace": "Energistics.Etp.v12.Datatypes.Object", "name": "ObjectChangeKind", "symbols": ["insert", "update", "authorized", "joined", "unjoined", "joinedSubscription", "unjoinedSubscription"], "fullName": "Energistics.Etp.v12.Datatypes.Object.ObjectChangeKind", "depends": []}'


class ObjectChangeKind(StrEnum):
    INSERT = "insert"
    UPDATE = "update"
    AUTHORIZED = "authorized"
    JOINED = "joined"
    UNJOINED = "unjoined"
    JOINED_SUBSCRIPTION = "joinedSubscription"
    UNJOINED_SUBSCRIPTION = "unjoinedSubscription"
