from typing import Optional

from chalk.client.client_impl import _ChalkAPIClientImpl
from chalk.client.client_protocol import (
    ChalkAPIClientProtocol,
    ChalkBaseException,
    ChalkError,
    ChalkException,
    ErrorCode,
    ErrorCodeCategory,
    FeatureResult,
    OfflineQueryContext,
    OnlineQueryContext,
    OnlineQueryResponse,
    WhoAmIResponse,
)
from chalk.features.feature import Feature

__all__ = [
    "ChalkError",
    "Feature",
    "FeatureResult",
    "WhoAmIResponse",
    "OnlineQueryResponse",
    "ChalkBaseException",
    "ChalkAPIClientProtocol",
    "OnlineQueryContext",
    "OfflineQueryContext",
    "ErrorCode",
    "ErrorCodeCategory",
    "ChalkException",
]


def ChalkClient(
    *,
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
    environment: Optional[str] = None,
    api_server: Optional[str] = None,
) -> ChalkAPIClientProtocol:
    return _ChalkAPIClientImpl(
        client_id=client_id,
        client_secret=client_secret,
        environment=environment,
        api_server=api_server,
    )
