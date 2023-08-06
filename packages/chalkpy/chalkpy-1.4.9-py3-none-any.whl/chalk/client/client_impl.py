import enum
import logging
from datetime import datetime
from itertools import chain
from typing import Any, Dict, List, Mapping, Optional, Tuple, Type, TypeVar, Union
from urllib.parse import urljoin

import pandas
import pandas as pd
import requests
from pydantic import BaseModel, ValidationError
from requests import HTTPError

from chalk.client.client_protocol import (
    ChalkAPIClientProtocol,
    ChalkBaseException,
    ChalkError,
    FeatureResult,
    OfflineQueryContext,
    OnlineQueryContext,
    OnlineQueryResponse,
    WhoAmIResponse,
)
from chalk.config.auth_config import load_token
from chalk.features import Feature
from chalk.features.feature import ChalkTime, FeatureWrapper, unwrap_feature
from chalk.serialization.codec import FeatureCodec

_logger = logging.getLogger(__name__)


class _ExchangeCredentialsRequest(BaseModel):
    client_id: str
    client_secret: str
    grant_type: str


class _ExchangeCredentialsResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    engines: Optional[Mapping[str, str]] = None


class _OfflineQueryResponse(BaseModel):
    columns: List[str]
    output: List[List[Any]]
    errors: Optional[List[ChalkError]]


class _OfflineQueryInput(BaseModel):
    columns: List[str]
    values: List[List[Any]]


class _OfflineQueryRequest(BaseModel):
    input: _OfflineQueryInput
    output: List[str]
    dataset: Optional[str] = None


class _QueryRequest(BaseModel):
    inputs: Mapping[str, Any]
    outputs: List[str]
    staleness: Optional[Mapping[str, str]] = None
    context: Optional[OnlineQueryContext]
    deployment_id: Optional[str] = None
    correlation_id: Optional[str] = None
    query_name: Optional[str] = None
    meta: Optional[Mapping[str, str]] = None


T = TypeVar("T")


class _ChalkClientConfig(BaseModel):
    client_id: str
    client_secret: str
    api_server: str
    active_environment: Optional[str]


class _OnlineQueryResponse(BaseModel):
    data: List[FeatureResult]
    errors: Optional[List[ChalkError]]


class ChalkOfflineQueryException(ChalkBaseException):
    message: str
    errors: List[ChalkError]

    def __init__(self, message: str, errors: List[ChalkError]):
        self.message = message
        self.errors = errors
        super().__init__(message + "\n" + "\n".join(["\t" + e.message for e in errors[0:3]]))


class OnlineQueryResponseWrapper(OnlineQueryResponse):
    data: List[FeatureResult]
    errors: Optional[List[ChalkError]]

    def __init__(
        self,
        data: List[FeatureResult],
        errors: Optional[List[ChalkError]],
        codec: FeatureCodec,
    ):
        self.data = data
        self.errors = errors
        self.codec = codec
        for d in self.data:
            if d.value is not None:
                d.value = codec.decode_fqn(d.field, d.value)
        self._values = {d.field: d for d in self.data}

    def get_feature(self, feature) -> Optional[FeatureResult]:
        return self._values.get(_get_feature_fqn(feature))

    def get_feature_value(self, feature) -> Optional[FeatureResult]:
        v = self.get_feature(feature)
        return v and v.value


def _get_feature_fqn(input: Union[str, Feature, FeatureWrapper]) -> str:
    if isinstance(input, FeatureWrapper):
        input = unwrap_feature(input)
    if isinstance(input, str):
        return input
    if isinstance(input, Feature):
        if len(input.path) > 0:
            return ".".join(
                chain(
                    (f"{x.parent.namespace}.{x.parent.name}" for x in input.path),
                    (input.name,),
                )
            )
        return input.fqn
    raise ValueError(f"Reference must be to a leaf feature. Received {input}.")


def _chunks(lst: list, chunk_size: int):
    for i in range(0, len(lst), chunk_size):
        yield lst[i : i + chunk_size]


class _ChalkAPIClientImpl(ChalkAPIClientProtocol):
    _headers: Optional[Tuple[Dict, Dict]]
    _config: _ChalkClientConfig
    _codec: FeatureCodec

    def __init__(
        self,
        *,
        client_id: Optional[str],
        client_secret: Optional[str],
        environment: Optional[str],
        api_server: Optional[str],
    ):
        if client_id is not None and client_secret is not None:
            self._config = _ChalkClientConfig(
                client_id=client_id,
                client_secret=client_secret,
                api_server=api_server or "https://api.chalk.ai",
                active_environment=environment,
            )
        else:
            token = load_token()
            if token is None:
                raise ValueError(
                    "Could not find .chalk.yml config file for project, "
                    "and explicit configuration was not provided. "
                    "You may need to run `chalk login` from your command line, "
                    "or check that your working directory is set to the root of "
                    "your project."
                )
            self._config = _ChalkClientConfig(
                client_id=token.clientId,
                client_secret=token.clientSecret,
                api_server=api_server or token.apiServer or "https://api.chalk.ai",
                active_environment=environment or token.activeEnvironment,
            )

        self._headers = None
        self._codec = FeatureCodec()

    def _exchange_credentials(self) -> _ExchangeCredentialsResponse:
        resp = requests.post(
            url=urljoin(self._config.api_server, f"v1/oauth/token"),
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            json=_ExchangeCredentialsRequest(
                client_id=self._config.client_id,
                client_secret=self._config.client_secret,
                grant_type="client_credentials",
            ).dict(),
            timeout=10,
        )
        try:
            response_json = resp.json()
            return _ExchangeCredentialsResponse(**response_json)
        except ValidationError:
            raise HTTPError(response_json)

    def _get_headers(self, environment_override: Optional[str], bust_cache: bool = False):
        if not bust_cache and self._headers is not None:
            _logger.debug("Returning cached authorization headers")
            return self._headers

        _logger.debug("Performing a credentials exchange")
        creds = self._exchange_credentials()

        self._headers = (
            {
                "Authorization": f"Bearer {creds.access_token}",
                "Accept": "application/json",
                "Content-Type": "application/json",
                "X-Chalk-Env-Id": environment_override or self._config.active_environment,
            },
            creds.engines or {},
        )

        return self._headers

    def _request(
        self,
        method: str,
        uri: str,
        response: Type[T],
        json: Optional[BaseModel] = None,
        use_engine: bool = False,
        environment_override: Optional[str] = None,
    ) -> T:
        x = self._get_headers(environment_override=environment_override)
        headers, engines = x
        base = (
            engines.get(
                environment_override or self._config.active_environment,
                self._config.api_server,
            )
            if use_engine
            else self._config.api_server
        )
        request = dict(
            method=method,
            url=urljoin(base, uri),
            json=json and json.dict(),
        )
        r = requests.request(headers=headers, **request)
        if r.status_code == 401:
            headers, _ = self._get_headers(environment_override=environment_override, bust_cache=True)
            r = requests.request(headers=headers, **request)

        r.raise_for_status()
        return response(**r.json())

    def whoami(self) -> WhoAmIResponse:
        return self._request(method="GET", uri=f"/v1/who-am-i", response=WhoAmIResponse)

    def query(
        self,
        input: Mapping[Union[str, Feature], Any],
        output: List[Union[str, Feature]],
        staleness: Optional[Mapping[Union[str, Feature], str]] = None,
        context: Optional[OnlineQueryContext] = None,
        preview_deployment_id: Optional[str] = None,
        correlation_id: Optional[str] = None,
        query_name: Optional[str] = None,
        meta: Optional[Mapping[str, str]] = None,
    ) -> OnlineQueryResponse:
        encoded_inputs = {}
        for feature, value in input.items():
            fqn = _get_feature_fqn(feature)
            encoded_inputs[fqn] = self._codec.encode_fqn(fqn, value)

        request = _QueryRequest(
            inputs=encoded_inputs,
            outputs=[_get_feature_fqn(f) for f in output],
            staleness=staleness and {_get_feature_fqn(k): v for k, v in staleness.items()},
            context=context,
            deployment_id=preview_deployment_id,
            correlation_id=correlation_id,
            query_name=query_name,
            meta=meta,
        )

        resp = self._request(
            method="POST",
            uri="/v1/query/online",
            json=request,
            response=_OnlineQueryResponse,
            use_engine=preview_deployment_id is None,
            environment_override=context.environment if context else None,
        )
        return OnlineQueryResponseWrapper(
            data=resp.data,
            errors=resp.errors,
            codec=self._codec,
        )

    def get_training_dataframe(
        self,
        input: Union[Mapping[Union[str, Feature], Any], pandas.DataFrame],
        input_times: List[datetime],
        output: List[Union[str, Feature]],
        context: Optional[OfflineQueryContext] = None,
        dataset: Optional[str] = None,
    ) -> pandas.DataFrame:
        if isinstance(input, Mapping):
            input = pandas.DataFrame(input)

        if isinstance(input, pandas.DataFrame):
            self._get_headers(environment_override=None)

        return self._get_training_dataframe(
            input=input,
            input_times=input_times,
            output=output,
            context=context,
            dataset=dataset,
        )

    def _decode_offline_response(self, offline_query_response) -> pandas.DataFrame:
        data = {}
        for col_index, column in enumerate(offline_query_response.output):
            series_values = []
            for value in column:
                value = self._codec.decode_fqn(
                    fqn=offline_query_response.columns[col_index],
                    value=value,
                )
                if isinstance(value, enum.Enum):
                    value = value.value
                series_values.append(value)

            data[offline_query_response.columns[col_index]] = pd.Series(
                series_values,
                dtype=self._codec.get_dtype(offline_query_response.columns[col_index]),
            )
        return pandas.DataFrame(data)

    def _get_training_dataframe(
        self,
        input: Union[Mapping[Union[str, Feature], Any], pandas.DataFrame],
        input_times: List[datetime],
        output: List[Union[str, Feature]],
        context: Optional[OfflineQueryContext] = None,
        dataset: Optional[str] = None,
    ) -> pandas.DataFrame:
        if isinstance(input, pandas.DataFrame):
            columns: List[Feature] = input.columns.values.tolist()
            matrix = input.T.values.tolist()

        elif isinstance(input, Mapping):
            columns = list(input.keys())
            matrix = list(input.values())

        else:
            raise ValueError("Expected a mapping or a pandas dataframe as input.")

        columns_fqn = [_get_feature_fqn(c) for c in chain(columns, (ChalkTime,))]

        matrix.append([a for a in input_times])

        for col_index, column in enumerate(matrix):
            for row_index, value in enumerate(column):
                matrix[col_index][row_index] = self._codec.encode_fqn(
                    fqn=columns_fqn[col_index],
                    value=value,
                )

        request = _OfflineQueryRequest(
            input=_OfflineQueryInput(
                columns=columns_fqn,
                values=matrix,
            ),
            output=[_get_feature_fqn(f) for f in output],
            dataset=dataset,
        )

        response = self._request(
            method="POST",
            uri="/v1/query/offline",
            json=request,
            response=_OfflineQueryResponse,
            use_engine=True,
            environment_override=context and context.environment,
        )

        if response.errors is not None and len(response.errors) > 0:
            raise ChalkOfflineQueryException(message="Failed while processing training query", errors=response.errors)

        return self._decode_offline_response(response)
