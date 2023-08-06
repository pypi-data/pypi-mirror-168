# -*- coding: utf-8 -*-

""" avro python class for file: rollback_transaction_response """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


from etptypes.energistics.etp.v12.datatypes.uuid import Uuid


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Protocol.Transaction", "name": "RollbackTransactionResponse", "protocol": "18", "messageType": "6", "senderRole": "store", "protocolRoles": "store,customer", "multipartFlag": false, "fields": [{"name": "transactionUuid", "type": {"type": "fixed", "namespace": "Energistics.Etp.v12.Datatypes", "name": "Uuid", "size": 16, "fullName": "Energistics.Etp.v12.Datatypes.Uuid", "depends": []}}, {"name": "successful", "type": "boolean", "default": true}, {"name": "failureReason", "type": "string", "default": ""}], "fullName": "Energistics.Etp.v12.Protocol.Transaction.RollbackTransactionResponse", "depends": ["Energistics.Etp.v12.Datatypes.Uuid"]}'


class RollbackTransactionResponse(ETPModel):

    transaction_uuid: Uuid = Field(alias="transactionUuid")

    successful: bool = Field(alias="successful", default=True)

    failure_reason: str = Field(alias="failureReason", default="")
