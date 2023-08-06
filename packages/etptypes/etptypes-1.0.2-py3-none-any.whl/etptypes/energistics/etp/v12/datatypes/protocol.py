# -*- coding: utf-8 -*-

""" avro python class for file: protocol """

import typing
from pydantic import validator
from etptypes import StrEnum


avro_schema: typing.Final[
    str
] = '{"type": "enum", "namespace": "Energistics.Etp.v12.Datatypes", "name": "Protocol", "symbols": ["Core", "ChannelStreaming", "ChannelDataFrame", "Discovery", "Store", "StoreNotification", "GrowingObject", "GrowingObjectNotification", "DEPRECATED_8", "DataArray", "RESERVED_10", "RESERVED_11", "RESERVED_12", "DiscoveryQuery", "StoreQuery", "RESERVED_15", "GrowingObjectQuery", "RESERVED_17", "Transaction", "RESERVED_19", "RESERVED_20", "ChannelSubscribe", "ChannelDataLoad", "RESERVED_23", "Dataspace", "SupportedTypes"], "fullName": "Energistics.Etp.v12.Datatypes.Protocol", "depends": []}'


class Protocol(StrEnum):
    CORE = "Core"
    CHANNEL_STREAMING = "ChannelStreaming"
    CHANNEL_DATA_FRAME = "ChannelDataFrame"
    DISCOVERY = "Discovery"
    STORE = "Store"
    STORE_NOTIFICATION = "StoreNotification"
    GROWING_OBJECT = "GrowingObject"
    GROWING_OBJECT_NOTIFICATION = "GrowingObjectNotification"
    DEPRECATED_8 = "DEPRECATED_8"
    DATA_ARRAY = "DataArray"
    RESERVED_10 = "RESERVED_10"
    RESERVED_11 = "RESERVED_11"
    RESERVED_12 = "RESERVED_12"
    DISCOVERY_QUERY = "DiscoveryQuery"
    STORE_QUERY = "StoreQuery"
    RESERVED_15 = "RESERVED_15"
    GROWING_OBJECT_QUERY = "GrowingObjectQuery"
    RESERVED_17 = "RESERVED_17"
    TRANSACTION = "Transaction"
    RESERVED_19 = "RESERVED_19"
    RESERVED_20 = "RESERVED_20"
    CHANNEL_SUBSCRIBE = "ChannelSubscribe"
    CHANNEL_DATA_LOAD = "ChannelDataLoad"
    RESERVED_23 = "RESERVED_23"
    DATASPACE = "Dataspace"
    SUPPORTED_TYPES = "SupportedTypes"
