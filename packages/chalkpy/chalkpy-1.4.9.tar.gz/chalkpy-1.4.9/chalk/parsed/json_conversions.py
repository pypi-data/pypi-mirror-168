import dataclasses
from types import NoneType
from typing import TypeVar, Union

import pydantic

from chalk.parsed.duplicate_input_gql import (
    KafkaConsumerConfigGQL,
    UpsertDataFrameGQL,
    UpsertFeatureGQL,
    UpsertFeatureIdGQL,
    UpsertFeatureReferenceGQL,
    UpsertFeatureTimeKindGQL,
    UpsertFilterGQL,
    UpsertHasManyKindGQL,
    UpsertHasOneKindGQL,
    UpsertReferencePathComponentGQL,
    UpsertResolverGQL,
    UpsertResolverOutputGQL,
    UpsertScalarKindGQL,
    UpsertSinkResolverGQL,
    UpsertStreamResolverGQL,
)
from chalk.parsed.feature import (
    DataFrameType,
    FeatureSetType,
    FeatureTimeFeatureType,
    FeatureType,
    FilterParsed,
    HasManyFeatureType,
    HasOneFeatureType,
    HasOnePathObjParsed,
    InputFeatureType,
    ScalarFeatureType,
)
from chalk.parsed.resolver import OfflineResolverParsed, OnlineResolverParsed, SinkResolverParsed
from chalk.streams.KafkaSource import KafkaConsumerConfig
from chalk.streams.stream import StreamResolver

T = TypeVar("T")


try:
    import attrs
except ImportError:
    attrs = None


def _get_feature_reference(f: FeatureType):
    return UpsertFeatureIdGQL(
        name=f.name,
        namespace=f.namespace,
        fqn=f.fqn,
    )


def _convert_filter_val(v: Union[T, ScalarFeatureType[T]]):
    if isinstance(v, ScalarFeatureType):
        return _get_feature_reference(v)
    raise ValueError("Haven't handled filters that aren't feature references")
    # return j("Scalar", dict(value=v))


def convert_type(t: T):
    if isinstance(t, KafkaConsumerConfig):
        return KafkaConsumerConfigGQL(
            broker=list(t.broker) if isinstance(t.broker, str) else t.broker,
            topic=list(t.topic) if isinstance(t.topic, str) else t.topic,
            ssl_keystore_location=t.ssl_keystore_location,
            client_id_prefix=t.client_id_prefix,
            group_id_prefix=t.group_id_prefix,
            topic_metadata_refresh_interval_ms=t.topic_metadata_refresh_interval_ms,
            security_protocol=t.security_protocol,
        )

    if isinstance(t, StreamResolver):
        return UpsertStreamResolverGQL(
            fqn=t.fqn,
            kind="stream",
            config=convert_type(t.source.consumer_config),
            function_definition=t.function_definition,
            environment=[t.environment] if isinstance(t.environment, str) else t.environment,
            doc=t.fn.__doc__,
        )

    if isinstance(t, HasManyFeatureType):
        return UpsertFeatureGQL(
            id=UpsertFeatureIdGQL(
                fqn=t.fqn,
                name=t.name,
                namespace=t.namespace,
            ),
            has_many_kind=UpsertHasManyKindGQL(
                columns=[convert_type(x).id for x in t.type.columns],
                filters=[convert_type(x).id for x in t.type.filters],
                join=convert_type(t.join),
            ),
            max_staleness=None,
            description=None,
            owner=None,
        )

    if isinstance(t, ScalarFeatureType):
        tags = [t.tags] if isinstance(t.tags, str) else t.tags
        assert isinstance(t.type, type)
        scalar_kind = t.type.__name__
        base_classes = [x.__name__ for x in type.mro(t.type)]

        # Attrs and Dataclasses don't technically have base classes
        # Pydantic calls their base class BaseModel which is way too generic for string comparsiion
        # For simplicity on the server-side validation, we'll come up with our own "base class" names
        if dataclasses.is_dataclass(t.type):
            base_classes.append("__dataclass__")
        if attrs is not None and isinstance(t.type, type) and attrs.has(t.type):
            base_classes.append("__attrs__")
        if issubclass(t.type, pydantic.BaseModel):
            base_classes.append("__pydantic__")

        return UpsertFeatureGQL(
            id=UpsertFeatureIdGQL(
                fqn=t.fqn,
                name=t.name,
                namespace=t.namespace,
            ),
            scalar_kind=UpsertScalarKindGQL(
                scalar_kind=scalar_kind,
                primary=t.primary,
                base_classes=base_classes,
                version=t.version,
                has_encoder_and_decoder=t.encoder is not None and t.decoder is not None,
            ),
            tags=tags,
            max_staleness=t.max_staleness,
            description=t.description,
            owner=t.owner,
            etl_offline_to_online=t.etl_offline_to_online,
        )

    if isinstance(t, HasOneFeatureType):
        return UpsertFeatureGQL(
            id=UpsertFeatureIdGQL(
                fqn=t.fqn,
                name=t.name,
                namespace=t.namespace,
            ),
            has_one_kind=UpsertHasOneKindGQL(join=convert_type(t.join)),
            max_staleness=None,
            description=None,
            owner=None,
        )

    if isinstance(t, FeatureTimeFeatureType):
        return UpsertFeatureGQL(
            id=UpsertFeatureIdGQL(
                fqn=t.fqn,
                name=t.name,
                namespace=t.namespace,
            ),
            feature_time_kind=UpsertFeatureTimeKindGQL(),
            max_staleness=None,
            description=None,
            owner=None,
        )

    if isinstance(t, FeatureSetType):
        return UpsertResolverOutputGQL(
            dataframes=[
                convert_type(f) for f in t.features if not isinstance(f, (FeatureTimeFeatureType, ScalarFeatureType))
            ],
            features=[
                _get_feature_reference(f)
                for f in t.features
                if isinstance(f, (FeatureTimeFeatureType, ScalarFeatureType))
            ],
        )

    if isinstance(t, DataFrameType):
        return UpsertDataFrameGQL(
            columns=[_get_feature_reference(f) for f in t.columns],
            filters=[convert_type(f) for f in t.filters],
        )

    if isinstance(t, FilterParsed):
        return UpsertFilterGQL(
            lhs=_convert_filter_val(t.lhs),
            op=t.operation,
            rhs=_convert_filter_val(t.rhs),
        )

    if isinstance(t, HasOnePathObjParsed):
        return UpsertReferencePathComponentGQL(
            parent=_get_feature_reference(t.parent),
            child=_get_feature_reference(t.child),
            parent_to_child_attribute_name=t.parent_to_child_attribute_name,
        )

    if isinstance(t, InputFeatureType):
        return UpsertFeatureReferenceGQL(
            underlying=_get_feature_reference(t.underlying),
            path=t.path and [convert_type(p) for p in t.path],
        )

    if isinstance(t, SinkResolverParsed):
        tags = [t.tags] if isinstance(t.tags, str) else t.tags

        resolver = UpsertSinkResolverGQL(
            fqn=t.fqn,
            function_definition=t.function_definition,
            inputs=[
                convert_type(i) if isinstance(i, InputFeatureType) else convert_type(InputFeatureType(i, list()))
                for i in t.inputs
            ],
            environment=t.environment,
            tags=tags,
            doc=t.doc,
            machine_type=t.machine_type,
            buffer_size=t.buffer_size,
            debounce=t.debounce,
            max_delay=t.max_delay,
            upsert=t.upsert,
        )
        return resolver

    if isinstance(t, (OfflineResolverParsed, OnlineResolverParsed)):
        assert isinstance(
            t.cron, (NoneType, (NoneType, str))
        ), f"Only supporting cron as a string right now for {t.fqn}"
        tags = [t.tags] if isinstance(t.tags, str) else t.tags

        resolver = UpsertResolverGQL(
            fqn=t.fqn,
            kind="offline" if isinstance(t, OfflineResolverParsed) else "online",
            function_definition=t.function_definition,
            inputs=[
                convert_type(i) if isinstance(i, InputFeatureType) else convert_type(InputFeatureType(i, list()))
                for i in t.inputs
            ],
            output=convert_type(t.output),
            environment=t.environment,
            tags=tags,
            doc=t.doc,
            cron=t.cron,
            machine_type=t.machine_type,
        )
        return resolver

    return t
