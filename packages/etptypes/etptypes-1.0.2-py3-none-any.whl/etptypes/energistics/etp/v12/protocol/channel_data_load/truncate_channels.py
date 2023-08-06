# -*- coding: utf-8 -*-

""" avro python class for file: truncate_channels """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


from etptypes.energistics.etp.v12.datatypes.channel_data.truncate_info import (
    TruncateInfo,
)


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Protocol.ChannelDataLoad", "name": "TruncateChannels", "protocol": "22", "messageType": "9", "senderRole": "customer", "protocolRoles": "store,customer", "multipartFlag": false, "fields": [{"name": "channels", "type": {"type": "map", "values": {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes.ChannelData", "name": "TruncateInfo", "fields": [{"name": "channelId", "type": "long"}, {"name": "newEndIndex", "type": {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "IndexValue", "fields": [{"name": "item", "type": ["null", "long", "double", {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes.ChannelData", "name": "PassIndexedDepth", "fields": [{"name": "pass", "type": "long"}, {"name": "direction", "type": {"type": "enum", "namespace": "Energistics.Etp.v12.Datatypes.ChannelData", "name": "PassDirection", "symbols": ["Up", "HoldingSteady", "Down"], "fullName": "Energistics.Etp.v12.Datatypes.ChannelData.PassDirection", "depends": []}}, {"name": "depth", "type": "double"}], "fullName": "Energistics.Etp.v12.Datatypes.ChannelData.PassIndexedDepth", "depends": ["Energistics.Etp.v12.Datatypes.ChannelData.PassDirection"]}]}], "fullName": "Energistics.Etp.v12.Datatypes.IndexValue", "depends": ["Energistics.Etp.v12.Datatypes.ChannelData.PassIndexedDepth"]}}], "fullName": "Energistics.Etp.v12.Datatypes.ChannelData.TruncateInfo", "depends": ["Energistics.Etp.v12.Datatypes.IndexValue"]}}}], "fullName": "Energistics.Etp.v12.Protocol.ChannelDataLoad.TruncateChannels", "depends": ["Energistics.Etp.v12.Datatypes.ChannelData.TruncateInfo"]}'


class TruncateChannels(ETPModel):

    channels: typing.Mapping[str, TruncateInfo] = Field(alias="channels")
