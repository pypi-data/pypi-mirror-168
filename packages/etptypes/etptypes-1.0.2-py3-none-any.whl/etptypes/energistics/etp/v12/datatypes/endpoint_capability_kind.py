# -*- coding: utf-8 -*-

""" avro python class for file: endpoint_capability_kind """

import typing
from pydantic import validator
from etptypes import StrEnum


avro_schema: typing.Final[
    str
] = '{"type": "enum", "namespace": "Energistics.Etp.v12.Datatypes", "name": "EndpointCapabilityKind", "symbols": ["ActiveTimeoutPeriod", "AuthorizationDetails", "ChangePropagationPeriod", "ChangeRetentionPeriod", "MaxConcurrentMultipart", "MaxDataObjectSize", "MaxPartSize", "MaxSessionClientCount", "MaxSessionGlobalCount", "MaxWebSocketFramePayloadSize", "MaxWebSocketMessagePayloadSize", "MultipartMessageTimeoutPeriod", "ResponseTimeoutPeriod", "RequestSessionTimeoutPeriod", "SessionEstablishmentTimeoutPeriod", "SupportsAlternateRequestUris", "SupportsMessageHeaderExtensions"], "fullName": "Energistics.Etp.v12.Datatypes.EndpointCapabilityKind", "depends": []}'


class EndpointCapabilityKind(StrEnum):
    ACTIVE_TIMEOUT_PERIOD = "ActiveTimeoutPeriod"
    AUTHORIZATION_DETAILS = "AuthorizationDetails"
    CHANGE_PROPAGATION_PERIOD = "ChangePropagationPeriod"
    CHANGE_RETENTION_PERIOD = "ChangeRetentionPeriod"
    MAX_CONCURRENT_MULTIPART = "MaxConcurrentMultipart"
    MAX_DATA_OBJECT_SIZE = "MaxDataObjectSize"
    MAX_PART_SIZE = "MaxPartSize"
    MAX_SESSION_CLIENT_COUNT = "MaxSessionClientCount"
    MAX_SESSION_GLOBAL_COUNT = "MaxSessionGlobalCount"
    MAX_WEB_SOCKET_FRAME_PAYLOAD_SIZE = "MaxWebSocketFramePayloadSize"
    MAX_WEB_SOCKET_MESSAGE_PAYLOAD_SIZE = "MaxWebSocketMessagePayloadSize"
    MULTIPART_MESSAGE_TIMEOUT_PERIOD = "MultipartMessageTimeoutPeriod"
    RESPONSE_TIMEOUT_PERIOD = "ResponseTimeoutPeriod"
    REQUEST_SESSION_TIMEOUT_PERIOD = "RequestSessionTimeoutPeriod"
    SESSION_ESTABLISHMENT_TIMEOUT_PERIOD = "SessionEstablishmentTimeoutPeriod"
    SUPPORTS_ALTERNATE_REQUEST_URIS = "SupportsAlternateRequestUris"
    SUPPORTS_MESSAGE_HEADER_EXTENSIONS = "SupportsMessageHeaderExtensions"
