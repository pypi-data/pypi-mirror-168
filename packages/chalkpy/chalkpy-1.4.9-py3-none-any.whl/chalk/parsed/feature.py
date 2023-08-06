from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Generator,
    Generic,
    List,
    Optional,
    Sequence,
    Set,
    Type,
    TypeVar,
    Union,
    cast,
)

from chalk.utils.collections import ensure_tuple, get_unique_item
from chalk.utils.duration import Duration

if TYPE_CHECKING:
    from chalk.features.feature import Feature

T = TypeVar("T")


class FeatureType(Generic[T]):
    def __init__(
        self,
        name: Optional[str],
        namespace: str,
        encoder: Optional[Callable[[T], Any]],
        decoder: Optional[Callable[[Any], T]],
        typ: Optional[Union[DataFrameType, Type[T]]],
        is_nullable: bool,
    ) -> None:
        self.name = name
        self.namespace = namespace
        self.encoder = encoder
        self.decoder = decoder
        self.type = typ
        self.is_nullable = is_nullable

    def is_scalar_primary(self) -> bool:
        return False

    def root_namespace(self) -> str:
        """The first component of the namespace.

        If the feature is an input feature, the root namespace should be the root namespace of the resolver.
        For example, if a resolver referenced ``Child.parent.name``, then this would be ``child``.

        Otherwise, this is equivalent to :attr:`namespace`.
        """
        return self.namespace

    def root_prefix(self) -> str:
        """The full namespace path, relative to the root, without the feature name.

        If the feature is an input feature, the rooted prefix will begin with the root namespace of the resolver,
        and contain the feature names of all relationships (except for the feature name in foreign features class).
        For example, if a resolver referenced ``Child.parent.name``, then this would be ``child.parent``.

        Otherwise, this is equivalent to :attr:`namespace`.
        """
        return self.namespace

    def root_fqn(self) -> str:
        """The fqn, relative to the root namespace.

        If the feature is an input feature, the rooted fqn will begin with the root namespace of the resolver,
        and contain all feature names of all relationships, including the feature name.
        For example, if a resolver referenced ``Child.parent.name``, then this would be ``child.parent.name``.

        Otherwise, this is equivalent to :attr:`fqn`.
        """
        return self.fqn

    @staticmethod
    def of(feature: Union[str, Feature, FeatureType]) -> "FeatureType":
        if isinstance(feature, FeatureType):
            return feature

        from chalk.parsed.conversions import DEFAULT_CONVERTER

        if isinstance(feature, str):
            raw_str = feature
            converted_feature = DEFAULT_CONVERTER.feature_from_string(raw_str)
            if converted_feature is None:
                raise ValueError(f'Could not resolve feature "{raw_str}"')
            feature = converted_feature

        return DEFAULT_CONVERTER.convert_target(feature)

    @property
    def fqn(self):
        if self.name is None:
            return self.namespace
        else:
            return f"{self.namespace}.{self.name}"

    def __str__(self):
        return self.root_fqn()

    def __repr__(self):
        return f"{type(self).__name__}(fqn={self.fqn}, type={str(self.type)})"

    def __hash__(self) -> int:
        return hash(self.fqn)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FeatureType):
            return NotImplemented
        if not isinstance(other, type(self)):
            return False
        return self.fqn == other.fqn


class InputFeatureType(FeatureType[T]):
    """FeatureType used to represent the children of has-one relationships. For"""

    def __init__(self, underlying: FeatureType[T], path: List[HasOnePathObjParsed]):
        super().__init__(
            name=underlying.name,
            namespace=underlying.namespace,
            encoder=None,
            decoder=None,
            typ=None,
            is_nullable=False,
        )
        assert not isinstance(
            underlying, InputFeatureType
        ), "Recursive InputFeaturetypes are disallowed. Instead, update the path."
        self.underlying = underlying
        self.path = path

    def walk_path_joins(self) -> Generator["HasOneFeatureType", Any, Any]:
        for x in self.path:
            yield x.parent

    def root_namespace(self) -> str:
        return self.path[0].parent.namespace

    def root_prefix(self) -> str:
        return self.root_namespace() + "." + ".".join(cast(str, x.parent.name) for x in self.path)

    def root_fqn(self):
        assert self.name is not None
        return self.root_prefix() + "." + self.name

    def __repr__(self):
        return f"InputFeatureType(fqn={self.underlying.fqn}, root_prefix={self.root_prefix()})"

    def __eq__(self, other):
        return isinstance(other, InputFeatureType) and other.underlying == self.underlying and self.path == other.path

    def __hash__(self):
        return self.underlying.__hash__()

    @property
    def join_path_keys(self) -> Set["ScalarFeatureType"]:
        ret = set()
        for p in self.path:
            ret.update(p.parent.join.referenced_features)
        return ret

    @property
    def join_path_spine(self) -> Set["ScalarFeatureType"]:
        ret = set()
        for p in self.path:
            ret.update([x for x in p.parent.join.referenced_features if x.namespace == p.parent.namespace])
        return ret

    @property
    def max_staleness(self):
        if isinstance(self.underlying, (ScalarFeatureType, InputFeatureType)):
            return self.underlying.max_staleness
        raise RuntimeError("Max staleness is not applicable")


class FeatureTimeFeatureType(FeatureType[datetime]):
    def __init__(self, name: str, namespace: str):
        super().__init__(
            name=name,
            namespace=namespace,
            encoder=None,
            decoder=None,
            typ=datetime,
            is_nullable=False,
        )


class ScalarFeatureType(FeatureType[T]):
    def is_scalar_primary(self) -> bool:
        return self.primary

    def __init__(
        self,
        name: str,
        namespace: str,
        type: Type[T],
        is_nullable: bool,
        is_list: bool,
        primary: bool = False,
        description: Optional[str] = None,
        version: Optional[int] = None,
        owner: Optional[str] = None,
        tags: Optional[Union[str, List[str]]] = None,
        max_staleness: Optional[Duration] = None,
        etl_offline_to_online: bool = False,
        encoder: Optional[Callable[[T], Any]] = None,
        decoder: Optional[Callable[[Any], T]] = None,
    ):
        super().__init__(
            namespace=namespace,
            name=name,
            encoder=encoder,
            decoder=decoder,
            typ=type,
            is_nullable=is_nullable,
        )
        self.is_list = is_list
        self.description = description
        self.owner = owner
        self.version = version
        self.tags = ensure_tuple(tags)
        self.primary = primary
        self.max_staleness = max_staleness
        self.etl_offline_to_online = etl_offline_to_online

    def required_by_join_path(self) -> Set[FeatureType]:
        return set()


@dataclass
class FilterParsed:
    lhs: Any
    operation: str
    rhs: Any

    def is_simple_join(self):
        return (
            isinstance(self.lhs, ScalarFeatureType)
            and isinstance(self.rhs, ScalarFeatureType)
            and self.operation == "=="
        )

    # If this filter is resolved relative to timestamps on the root query (or 'now') then we need
    # to handle it per-row in a fancy way
    def is_constant_filter(self) -> bool:
        from chalk.features.feature import TimeDelta

        referenced_time_delta = isinstance(self.lhs, TimeDelta) or isinstance(self.rhs, TimeDelta)
        return not referenced_time_delta

    @property
    def referenced_features(self) -> Set[ScalarFeatureType]:
        return set(v for v in (self.lhs, self.rhs) if isinstance(v, ScalarFeatureType))


class HasOneFeatureType(FeatureType[T]):
    def __init__(self, namespace: str, name: str, join: FilterParsed, is_nullable: bool):
        super().__init__(
            namespace=namespace,
            name=name,
            encoder=None,
            decoder=None,
            typ=None,
            is_nullable=is_nullable,
        )
        self.join = join

    # this will be replaced once support for multiple join conditions is fully implemented
    def only_local_feature(self) -> ScalarFeatureType:
        return self.local_features()[0]

    # this will be replaced once support for multiple join conditions is fully implemented
    def only_foreign_features(self) -> ScalarFeatureType:
        return self.foreign_features()[0]

    def local_features(self) -> List[ScalarFeatureType]:
        return list(filter(lambda x: x.namespace == self.namespace, self.join.referenced_features))

    def foreign_features(self) -> List[ScalarFeatureType]:
        return list(filter(lambda x: x.namespace != self.namespace, self.join.referenced_features))

    def foreign_namespace(self) -> str:
        return next(iter(self.foreign_features())).namespace

    def get_first_level_scalars(self):
        assert isinstance(self.type, FeatureSetType)
        return [f for f in self.type.features if isinstance(f, ScalarishFeatureType)]

    def __eq__(self, other):
        return (
            isinstance(other, HasOneFeatureType)
            and self.name == other.name
            and self.namespace == other.namespace
            and self.join == other.join
        )

    def __hash__(self):
        # FIXME(Andy) (need to come up with a unique hash)
        return hash((self.name, self.namespace))


class DataFrameType(FeatureType[None]):
    def __init__(self, filters: List[FilterParsed], columns: List[QueryInputType]):
        namespaces = [x.root_namespace() for x in columns]
        namespace = get_unique_item(namespaces, name="dataframe column namespace")
        super().__init__(
            encoder=None,
            decoder=None,
            typ=None,
            name=None,
            namespace=namespace,
            is_nullable=False,
        )
        self.filters = filters
        self.columns = columns

    def __repr__(self):
        return f"DataFrameType(namespace={self.namespace}, filters={str(self.filters)}, columns={str(self.columns)})"

    def __hash__(self):
        return hash((tuple(self.filters), tuple(self.columns)))

    def __eq__(self, other):
        if not isinstance(other, DataFrameType):
            return NotImplemented

        return self.filters == other.filters and self.columns == other.columns

    def all_referenced_features(self) -> Set[FeatureType]:
        ret: Set[FeatureType] = set()

        ret.update(self.columns)

        for filter in self.filters:
            if isinstance(filter.lhs, ScalarFeatureType):
                ret.add(filter.lhs)

            if isinstance(filter.rhs, ScalarFeatureType):
                ret.add(filter.rhs)

        return ret


class FeatureSetType(FeatureType[T]):
    def __init__(self, features: Sequence[FeatureType[T]]) -> None:
        namespaces = [f.namespace for f in features]
        namespace = get_unique_item(namespaces, name="feature namespace")
        super().__init__(
            name=None,
            namespace=namespace,
            encoder=None,
            decoder=None,
            typ=None,
            is_nullable=False,
        )
        assert len(features) > 0
        self.features = features

    def __eq__(self, other):
        return isinstance(other, FeatureSetType) and self.features == other.features

    def __hash__(self):
        return hash(tuple(self.features))

    def is_single_data_frame(self) -> bool:
        return len(self.features) == 1 and isinstance(self.features[0], DataFrameType)

    def get_first_level_scalars(self):
        return [f for f in self.features if isinstance(f, ScalarishFeatureType)]


class HasManyFeatureType(FeatureType[DataFrameType]):
    join: FilterParsed

    def __init__(
        self,
        namespace: str,
        name: str,
        join: FilterParsed,
        type: Optional[DataFrameType],
    ):
        super().__init__(
            namespace=namespace,
            name=name,
            encoder=None,
            decoder=None,
            typ=type,
            is_nullable=False,
        )
        self.join = join

    def __eq__(self, other):
        if not isinstance(other, HasManyFeatureType):
            return NotImplemented

        namespace_eq = self.namespace == other.namespace
        name_eq = self.name == other.name

        if namespace_eq and name_eq:
            # trivial perf opt...
            type_eq = self.type == other.type
            join_eq = self.join == other.join
            return type_eq and join_eq
        else:
            return False

    def __hash__(self) -> int:
        return super().__hash__()

    def local_features(self) -> List[FeatureType]:
        return list(filter(lambda x: x.namespace == self.namespace, self.join.referenced_features))

    def foreign_features(self) -> List[FeatureType]:
        return list(filter(lambda x: x.namespace != self.namespace, self.join.referenced_features))

    def foreign_namespace(self) -> str:
        return next(
            filter(lambda x: x.namespace != self.namespace, self.join.referenced_features),
        ).namespace


JoinFeatureType = Union[HasOneFeatureType, HasManyFeatureType]


@dataclass
class HasOnePathObjParsed:
    parent: HasOneFeatureType
    # The final child in a path will not be a HasOneFeatureType,
    # and all other intermediate children will be HasOneFeatureType
    child: FeatureType
    parent_to_child_attribute_name: str

    def __hash__(self):
        return hash((self.parent.fqn, self.parent_to_child_attribute_name))

    def __eq__(self, other):
        return (
            isinstance(other, HasOnePathObjParsed)
            and self.parent_to_child_attribute_name == other.parent_to_child_attribute_name
            and self.parent == other.parent
            and self.child == other.child
        )


ScalarishFeatureType = Union[ScalarFeatureType, FeatureTimeFeatureType]
QueryInputType = Union[ScalarishFeatureType, HasManyFeatureType, HasOneFeatureType, InputFeatureType]
QueryOutputType = Union[ScalarishFeatureType, HasManyFeatureType, InputFeatureType]
TIMESTAMP = ScalarFeatureType(
    namespace="global__",
    name="global_timestamp__",
    description="Timestamp Field",
    primary=False,
    type=datetime,
    is_nullable=False,
    is_list=False,
)
