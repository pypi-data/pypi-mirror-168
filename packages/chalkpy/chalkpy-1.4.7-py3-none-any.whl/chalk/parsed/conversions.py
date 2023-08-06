import inspect
import weakref
from datetime import datetime
from typing import Any, List, Optional, Type, TypeVar, Union, overload

from chalk.features import DataFrame, Feature, Filter
from chalk.features.feature import Features, FeatureSetBase, FeatureWrapper, HasOnePathObj, unwrap_feature
from chalk.features.resolver import Cron, OfflineResolver, OnlineResolver, SinkResolver
from chalk.features.tag import Tags
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
from chalk.parsed.resolver import (
    CronFilterWithFeatureArgs,
    OfflineResolverParsed,
    OnlineResolverParsed,
    SinkResolverParsed,
)
from chalk.utils.duration import ScheduleOptions

T = TypeVar("T")
TFeatureType = TypeVar("TFeatureType", bound=FeatureType)


class APIToProcessorConverter:
    def __init__(self):
        self._cache = weakref.WeakKeyDictionary()

    def _convert_filter(self, f: Union[Filter, FilterParsed]) -> FilterParsed:
        if isinstance(f, FilterParsed):
            return f

        def convert_if_feature(v: Any):
            if isinstance(v, Feature):
                return self._convert_scalar_feature(v)
            elif isinstance(v, Filter):
                return self._convert_filter(v)
            return v

        return FilterParsed(
            lhs=convert_if_feature(f.feature),
            operation=f.operation,
            rhs=convert_if_feature(f.other),
        )

    def _convert_scalar_feature(self, f: Feature) -> ScalarFeatureType:
        cached_val = self._cache.get(f)
        if cached_val is not None:
            assert isinstance(cached_val, ScalarFeatureType)
            return cached_val

        if f.name is None or f.namespace is None:
            raise ValueError(f"Referenced feature is missing namespace or name {f.namespace}.{f.name}.")

        if f.typ is None:
            raise ValueError(f"Feature missing type {f.namespace}.{f.name}")

        converted = ScalarFeatureType(
            name=f.name,
            namespace=f.namespace,
            type=f.typ.underlying,
            is_nullable=f.typ.is_nullable,
            is_list=f.typ.is_list,
            primary=f.primary,
            version=f.version,
            description=f.description,
            owner=f.owner,
            tags=f.tags,
            max_staleness=f.max_staleness,
            etl_offline_to_online=f.etl_offline_to_online,
            encoder=f.encoder,
            decoder=f.decoder,
        )
        self._cache[f] = converted
        return converted

    @staticmethod
    def _convert_feature_time(t: Feature) -> FeatureTimeFeatureType:
        assert t.is_feature_time
        assert t.typ is not None
        assert issubclass(t.typ.underlying, datetime)
        assert t.name is not None
        assert t.namespace is not None
        return FeatureTimeFeatureType(t.name, t.namespace)

    def _convert_has_one(self, f: Feature) -> HasOneFeatureType:
        assert f.is_has_one
        if self._cache.get(f) is not None:
            val = self._cache.get(f)
            assert isinstance(val, HasOneFeatureType)
            return val

        if f.name is None or f.namespace is None:
            raise ValueError(f"Feature wasn't named {f.namespace}.{f.name}")

        if f.typ is None:
            raise ValueError(f"Feature missing typ {f.namespace}.{f.name}")

        if f.join is None:
            raise ValueError(f"Feature missing join {f.namespace}.{f.name}")

        assert issubclass(f.typ.underlying, Features), "has-one relationships must reference a Features cls"
        ret = HasOneFeatureType(
            namespace=f.namespace,
            name=f.name,
            join=self._convert_filter(f.join),
            is_nullable=f.typ.is_nullable,
        )
        self._cache[f] = ret
        ret.type = self.convert_type(f.typ.underlying)
        return ret

    def _convert_has_many(self, f: Feature) -> HasManyFeatureType:
        assert f.is_has_many
        cached_val = self._cache.get(f)
        if cached_val is not None:
            assert isinstance(cached_val, HasManyFeatureType)
            return cached_val

        if f.name is None or f.namespace is None:
            raise ValueError(f"Feature wasn't named: {f.namespace}.{f.name}")

        assert f.join is not None, "has many feature type should have join"
        assert f.typ is not None, "type should be defined"

        ret = HasManyFeatureType(
            namespace=f.namespace,
            name=f.name,
            join=self._convert_filter(f.join),
            type=None,
        )
        self._cache[f] = ret
        parsed_annotation = f.typ.parsed_annotation
        assert issubclass(parsed_annotation, DataFrame)
        converted_type = self.convert_type(parsed_annotation)
        assert isinstance(converted_type, DataFrameType)
        ret.type = converted_type
        return ret

    def _convert_environment(self, e: Optional[Union[List[str], str]]) -> Optional[List[str]]:
        return [e] if isinstance(e, str) else e

    def _convert_tags(self, tags: Optional[Tags]) -> Optional[List[str]]:
        if tags is None:
            return None
        if isinstance(tags, list):
            return tags
        if isinstance(tags, str):
            return [tags]
        raise ValueError("Tags should be a list of strings or a string or None")

    def _convert_path(self, o: Feature) -> List[HasOnePathObjParsed]:
        return [self._convert_has_one_path_obj(p) for p in o.path]

    def _wrap_as_input_ft(self, converted: TFeatureType, raw: Feature) -> Union[InputFeatureType, TFeatureType]:
        """"""
        if len(raw.path) < 1:
            return converted

        i = InputFeatureType(underlying=converted, path=self._convert_path(raw))
        return i

    def feature_from_string(self, s: str) -> Optional[Feature]:
        split = s.split(".")
        current = None
        if len(split) > 0:
            base = FeatureSetBase.registry.get(split[0])
            current = base
            for p in split[1:]:
                if current is not None:
                    try:
                        current = getattr(current, p)
                    except AttributeError:
                        current = None
        if isinstance(current, FeatureWrapper):
            current = unwrap_feature(current)
        assert current is None or isinstance(current, Feature)
        return current

    def convert_target(self, raw: Union[Feature, FeatureWrapper]) -> FeatureType:
        if isinstance(raw, FeatureWrapper):
            raw = unwrap_feature(raw)
        converted = self.convert_type(raw)
        return self._wrap_as_input_ft(converted, raw)

    def _convert_has_one_path_obj(self, t: HasOnePathObj) -> HasOnePathObjParsed:
        parent = self.convert_type(t.parent)
        assert isinstance(parent, HasOneFeatureType)
        return HasOnePathObjParsed(
            parent=parent,
            child=self.convert_type(t.child),
            parent_to_child_attribute_name=t.parent_to_child_attribute_name,
        )

    def _convert_sink_resolver(self, r: SinkResolver) -> SinkResolverParsed:
        return SinkResolverParsed(
            function_definition=r.function_definition,
            filename=r.filename,
            fqn=r.fqn,
            doc=r.doc,
            inputs=[self._wrap_as_input_ft(self.convert_type(i), i) for i in r.inputs],
            raw_fn=r.fn,
            environment=self._convert_environment(r.environment),
            tags=self._convert_tags(r.tags),
            machine_type=r.machine_type,
            buffer_size=r.buffer_size,
            debounce=r.debounce,
            max_delay=r.max_delay,
            upsert=r.upsert,
        )

    def _convert_cron_filter(self, cron: Optional[Union[ScheduleOptions, Cron]]) -> Optional[CronFilterWithFeatureArgs]:
        if cron is not None and isinstance(cron, Cron) and cron.filter is not None:
            sig = inspect.signature(cron.filter)
            filter_features = [FeatureType.of(parameter.annotation) for parameter in sig.parameters.values()]
            return CronFilterWithFeatureArgs(
                filter=cron.filter,
                feature_args=filter_features,
            )
        else:
            return None

    def _convert_offline_resolver(self, r: OfflineResolver) -> OfflineResolverParsed:
        output = self.convert_type(r.output)
        return OfflineResolverParsed(
            function_definition=r.function_definition,
            filename=r.filename,
            fqn=r.fqn,
            doc=r.doc,
            inputs=[self._wrap_as_input_ft(self.convert_type(i), i) for i in r.inputs],
            output=output,
            raw_fn=r.fn,
            fn=r.fn,
            environment=self._convert_environment(r.environment),
            tags=self._convert_tags(r.tags),
            cron=r.cron,
            cron_filter=self._convert_cron_filter(r.cron),
            machine_type=r.machine_type,
        )

    def _convert_online_resolver(self, r: OnlineResolver) -> OnlineResolverParsed:
        output = self.convert_type(r.output)
        return OnlineResolverParsed(
            function_definition=r.function_definition,
            filename=r.filename,
            fqn=r.fqn,
            doc=r.doc,
            inputs=[self._wrap_as_input_ft(self.convert_type(i), i) for i in r.inputs],
            output=output,
            raw_fn=r.fn,
            fn=r.fn,
            environment=self._convert_environment(r.environment),
            tags=self._convert_tags(r.tags),
            cron=r.cron,
            cron_filter=self._convert_cron_filter(r.cron),
            machine_type=r.machine_type,
            when=self._convert_filter(r.when) if r.when is not None else None,
        )

    @overload
    def convert_type(
        self,
        t: Union[Feature, FeatureWrapper],
    ) -> Union[HasOneFeatureType, HasManyFeatureType, FeatureTimeFeatureType, ScalarFeatureType]:
        ...

    @overload
    def convert_type(
        self,
        t: FeatureType[T],
        parent: Optional[Feature] = None,
    ) -> FeatureType[T]:
        ...

    @overload
    def convert_type(
        self,
        t: Type[DataFrame],
    ) -> DataFrameType:
        ...

    @overload
    def convert_type(
        self,
        t: Type[Features],
    ) -> FeatureSetType:
        ...

    @overload
    def convert_type(self, t: Union[OnlineResolver, OnlineResolverParsed]) -> OnlineResolverParsed:
        ...

    @overload
    def convert_type(self, t: Union[OfflineResolver, OfflineResolverParsed]) -> OfflineResolverParsed:
        ...

    @overload
    def convert_type(self, t: Union[SinkResolver, SinkResolverParsed]) -> SinkResolverParsed:
        ...

    @overload
    def convert_type(self, t: Union[HasOnePathObj, HasOnePathObjParsed]) -> HasOnePathObjParsed:
        ...

    def convert_type(
        self,
        t,
    ):
        if isinstance(t, type):
            if issubclass(t, DataFrame):
                cols = [self._wrap_as_input_ft(self.convert_type(f), f) for f in t.columns]
                column_filters = [self._convert_filter(f) for f in t.filters]
                return DataFrameType(columns=cols, filters=column_filters)

            if issubclass(t, Features):
                return FeatureSetType[Any](
                    features=[self.convert_type(f) for f in t.features],
                )

        if isinstance(t, FeatureWrapper):
            t = unwrap_feature(t)

        if isinstance(t, Feature):
            assert t.typ is not None

            if t.is_has_one:
                return self._convert_has_one(t)

            elif t.is_has_many:
                return self._convert_has_many(t)

            elif t.is_feature_time:
                return self._convert_feature_time(t)

            else:
                return self._convert_scalar_feature(t)

        if isinstance(t, OnlineResolver):
            return self._convert_online_resolver(t)

        if isinstance(t, OfflineResolver):
            return self._convert_offline_resolver(t)

        if isinstance(t, HasOnePathObj):
            return self._convert_has_one_path_obj(t)

        if isinstance(t, SinkResolver):
            return self._convert_sink_resolver(t)

        if isinstance(
            t,
            (
                FeatureType,
                HasOnePathObjParsed,
                DataFrameType,
                FeatureSetType,
                OnlineResolverParsed,
                OfflineResolverParsed,
                SinkResolverParsed,
            ),
        ):
            return t

        raise TypeError(f"Unexpected type: {t}")


DEFAULT_CONVERTER = APIToProcessorConverter()
