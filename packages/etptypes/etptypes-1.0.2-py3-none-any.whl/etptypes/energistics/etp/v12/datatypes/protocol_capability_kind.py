# -*- coding: utf-8 -*-

""" avro python class for file: protocol_capability_kind """

import typing
from pydantic import validator
from etptypes import StrEnum


avro_schema: typing.Final[
    str
] = '{"type": "enum", "namespace": "Energistics.Etp.v12.Datatypes", "name": "ProtocolCapabilityKind", "symbols": ["FrameChangeDetectionPeriod", "MaxDataArraySize", "MaxDataObjectSize", "MaxFrameResponseRowCount", "MaxIndexCount", "MaxRangeChannelCount", "MaxRangeDataItemCount", "MaxResponseCount", "MaxStreamingChannelsSessionCount", "MaxSubscriptionSessionCount", "MaxTransactionCount", "SupportsSecondaryIndexFiltering", "TransactionTimeoutPeriod"], "fullName": "Energistics.Etp.v12.Datatypes.ProtocolCapabilityKind", "depends": []}'


class ProtocolCapabilityKind(StrEnum):
    FRAME_CHANGE_DETECTION_PERIOD = "FrameChangeDetectionPeriod"
    MAX_DATA_ARRAY_SIZE = "MaxDataArraySize"
    MAX_DATA_OBJECT_SIZE = "MaxDataObjectSize"
    MAX_FRAME_RESPONSE_ROW_COUNT = "MaxFrameResponseRowCount"
    MAX_INDEX_COUNT = "MaxIndexCount"
    MAX_RANGE_CHANNEL_COUNT = "MaxRangeChannelCount"
    MAX_RANGE_DATA_ITEM_COUNT = "MaxRangeDataItemCount"
    MAX_RESPONSE_COUNT = "MaxResponseCount"
    MAX_STREAMING_CHANNELS_SESSION_COUNT = "MaxStreamingChannelsSessionCount"
    MAX_SUBSCRIPTION_SESSION_COUNT = "MaxSubscriptionSessionCount"
    MAX_TRANSACTION_COUNT = "MaxTransactionCount"
    SUPPORTS_SECONDARY_INDEX_FILTERING = "SupportsSecondaryIndexFiltering"
    TRANSACTION_TIMEOUT_PERIOD = "TransactionTimeoutPeriod"
