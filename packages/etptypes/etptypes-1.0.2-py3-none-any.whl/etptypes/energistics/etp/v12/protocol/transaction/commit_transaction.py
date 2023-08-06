# -*- coding: utf-8 -*-

""" avro python class for file: commit_transaction """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


from etptypes.energistics.etp.v12.datatypes.uuid import Uuid


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Protocol.Transaction", "name": "CommitTransaction", "protocol": "18", "messageType": "3", "senderRole": "customer", "protocolRoles": "store,customer", "multipartFlag": false, "fields": [{"name": "transactionUuid", "type": {"type": "fixed", "namespace": "Energistics.Etp.v12.Datatypes", "name": "Uuid", "size": 16, "fullName": "Energistics.Etp.v12.Datatypes.Uuid", "depends": []}}], "fullName": "Energistics.Etp.v12.Protocol.Transaction.CommitTransaction", "depends": ["Energistics.Etp.v12.Datatypes.Uuid"]}'


class CommitTransaction(ETPModel):

    transaction_uuid: Uuid = Field(alias="transactionUuid")
