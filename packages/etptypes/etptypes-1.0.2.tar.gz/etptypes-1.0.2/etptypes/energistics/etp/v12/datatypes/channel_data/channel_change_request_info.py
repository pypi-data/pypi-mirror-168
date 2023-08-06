# -*- coding: utf-8 -*-

""" avro python class for file: channel_change_request_info """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Datatypes.ChannelData", "name": "ChannelChangeRequestInfo", "fields": [{"name": "sinceChangeTime", "type": "long"}, {"name": "channelIds", "type": {"type": "array", "items": "long"}}], "fullName": "Energistics.Etp.v12.Datatypes.ChannelData.ChannelChangeRequestInfo", "depends": []}'


class ChannelChangeRequestInfo(ETPModel):

    since_change_time: int = Field(alias="sinceChangeTime")

    channel_ids: typing.List[Strict[int]] = Field(alias="channelIds")
