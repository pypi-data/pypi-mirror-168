from __future__ import annotations

import collections.abc
import copy
import dataclasses
import types
from datetime import datetime, timedelta
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    ClassVar,
    Dict,
    List,
    Optional,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
    get_args,
    get_origin,
    get_type_hints,
)

from chalk.features.tag import Tags
from chalk.utils.collections import ensure_tuple, get_unique_item
from chalk.utils.duration import Duration

if TYPE_CHECKING:
    from chalk.features.dataframe import DataFrame
    from chalk.parsed.feature import FeatureType


U = TypeVar("U")
JsonValue = TypeVar("JsonValue")


class FeatureTypeAnnotation:
    def __init__(
        self,
        features_cls: Optional[Type[Features]] = None,
        attribute_name: Optional[str] = None,
        *,
        underlying: Optional[type] = None,
    ) -> None:
        # Either pass in the underlying -- if it is already parsed -- or pass in the feature cls and attribute name

        self._features_cls = features_cls
        self._attribute_name = attribute_name
        self._is_nullable = None
        self._is_dataframe = None
        self._is_list = None
        self._is_scalar = None
        self._underlying = None
        self._parsed_annotation = None
        if underlying is not None:
            if features_cls is not None and attribute_name is not None:
                raise ValueError("If specifying the underlying, do not specify (features_cls, attribute_name)")
            self._parse_type(underlying)
        else:
            if features_cls is None or attribute_name is None:
                raise ValueError(
                    "If not specifying the underlying, then both the (features_cls, attribute_name) must be provided"
                )
        # Store the class and attribute name so we can later use typing.get_type_hints to
        # resolve any forward references in the type annotations
        # Resolution happens lazily -- after everything is imported -- to avoid circular imports

    @property
    def is_parsed(self) -> bool:
        return self._underlying is not None

    @property
    def annotation(self) -> Union[str, type]:
        """Return the type annotation, without parsing the underlying type if it is not yet already parsed."""
        if self._parsed_annotation is not None:
            # It is already parsed. Return it.
            return self._parsed_annotation
        assert self._features_cls is not None
        assert self._attribute_name is not None
        return self._features_cls.__annotations__[self._attribute_name]

    @property
    def parsed_annotation(self) -> type:
        """The parsed type annotation. It will be parsed if needed.

        Unlike :attr:`underlying`, parsed annotation contains any container or optional types, such as
        list, dataframe, or Optional.
        """
        if self._parsed_annotation is None:
            self._parse_annotation()
        assert self._parsed_annotation is not None
        return self._parsed_annotation

    def __str__(self):
        if isinstance(self.annotation, type):
            return self.annotation.__name__
        else:
            return str(self.annotation)

    def _parse_annotation(self):
        assert self._features_cls is not None
        assert self._attribute_name is not None
        hints = get_type_hints(self._features_cls)
        parsed_annotation = hints[self._attribute_name]
        self._parse_type(parsed_annotation)

    def _parse_type(self, annotation: Optional[type]):
        from chalk.features.dataframe import DataFrame

        assert self._parsed_annotation is None, "The annotation was already parsed"
        self._parsed_annotation = annotation
        origin = get_origin(annotation)
        self._is_nullable = False
        if self._features_cls is not None and self._attribute_name is not None:
            # Return a more helpful error message, since we have context
            error_ctx = f" {self._features_cls.__name__}.{self._attribute_name}"
        else:
            error_ctx = ""
        if origin in (
            Union,
            getattr(types, "UnionType", Union),
        ):  # using getattr as UnionType was introduced in python 3.10
            args = get_args(annotation)
            # If it's a union, then the only supported union is for nullable features. Validate this
            if len(args) != 2 or (None not in args and type(None) not in args):
                raise TypeError(
                    f"Invalid annotation for feature{error_ctx}: Unions with non-None types are not allowed"
                )
            annotation = args[0] if args[1] in (None, type(None)) else args[1]
            self._is_nullable = True

        # The only allowed collections here are List or DataFrame
        self._is_list = False
        if origin in (list, List):
            args = get_args(annotation)
            assert len(args) == 1, "typing.List takes just one arg"
            annotation = args[0]
            self._is_list = True

        self._is_dataframe = False
        if annotation is not None and issubclass(annotation, DataFrame):
            self._is_dataframe = True
            # For features, annotations like DataFrame[User.id] are not allowed
            # Annotations like these are only allowed in resolvers
            # So, error here.
            # if annotation.references_feature_set is None:
            #     raise TypeError("DF has no underlying type")
            annotation = annotation.references_feature_set

        self._is_scalar = annotation is not None and not issubclass(annotation, Features)

        if self._is_list and not self._is_scalar:
            raise TypeError(
                f"Invalid type annotation for feature{error_ctx}: Lists must be of scalar types, not {self._parsed_annotation}"
            )
        if self._is_dataframe and self._is_scalar:
            raise TypeError(
                f"Invalid type annotation for feature{error_ctx}: Dataframes must be of Features types, not {self._parsed_annotation}"
            )

        self._underlying = annotation

    @property
    def is_nullable(self) -> bool:
        """Whether the type annotation is nullable."""
        if self._parsed_annotation is None:
            self._parse_annotation()
        assert self._is_nullable is not None
        return self._is_nullable

    @property
    def underlying(self) -> type:
        """The underlying type annotation from the annotation."""
        if self.parsed_annotation is None:
            self._parse_annotation()
        if self._underlying is None:
            raise TypeError("There is no underlying type")
        return self._underlying

    @underlying.setter
    def underlying(self, underlying: Optional[type]):
        self._underlying = underlying

    @property
    def is_dataframe(self) -> bool:
        """Whether the type annotation is a dataframe."""
        if self._parsed_annotation is None:
            self._parse_annotation()
        assert self._is_dataframe is not None
        return self._is_dataframe

    @property
    def is_list(self) -> bool:
        """Whether the type annotation is a list."""
        if self._parsed_annotation is None:
            self._parse_annotation()
        assert self._is_list is not None
        return self._is_list

    @property
    def is_scalar(self) -> bool:
        """Whether the type annotation is a scalar type (i.e. not a Features type)."""
        if self._parsed_annotation is None:
            self._parse_annotation()
        assert self._is_scalar is not None
        return self._is_scalar


@dataclasses.dataclass
class HasOnePathObj:
    parent: Feature
    child: Feature
    parent_to_child_attribute_name: str


class FeatureWrapper:
    """The FeatureWrapper emulates DataFrames and nested has-one relationships when used as a type annotation or within a filter."""

    def __init__(self, feature: Feature) -> None:
        # Binding as a private variable as not to have naming conflicts user's use of __getattr__
        self._chalk_feature = feature

    def __hash__(self):
        return id(self)

    def __gt__(self, other):
        return Filter(self, ">", other)

    def __ge__(self, other):
        return Filter(self, ">=", other)

    def __lt__(self, other):
        return Filter(self, "<", other)

    def __le__(self, other):
        return Filter(self, "<=", other)

    def __ne__(self, other):
        return Filter(self, "!=", other)

    def __eq__(self, other):
        return Filter(self, "==", other)

    def __and__(self, other):
        return Filter(self, "and", other)

    def __or__(self, other):
        return Filter(self, "or", other)

    def __repr__(self):
        return f"FeatureWrapper(fqn={self._chalk_feature.namespace}.{self._chalk_feature.name}, typ={self._chalk_feature.typ})"

    def __str__(self):
        return str(self._chalk_feature)

    def in_(self, examples):
        return Filter(self._chalk_feature, "in", examples)

    def __getitem__(self, item):
        from chalk.df.ChalkASTParser import ChalkASTParser
        from chalk.features.dataframe import DataFrame

        if self._chalk_feature.typ is not None and issubclass(self._chalk_feature.typ.parsed_annotation, DataFrame):
            f_copy = FeatureWrapper(copy.copy(self._chalk_feature))

            with ChalkASTParser.ignore_ast_parse_errors():
                f_copy._chalk_feature.typ = FeatureTypeAnnotation(
                    underlying=self._chalk_feature.typ.parsed_annotation[item]
                )

            return f_copy
        raise TypeError(f"Feature {self} is not subscriptable.")

    def __getattr__(self, item: str):
        # Passing through __getattr__ on has_one features, as users can use getattr
        # notation in annotations for resolvers
        if item.startswith("__"):
            # Short-circuiting on the dunders to be compatible with copy.copy
            raise AttributeError(item)
        if self._chalk_feature.typ is not None and issubclass(self._chalk_feature.typ.underlying, Features):
            for f in self._chalk_feature.typ.underlying.features:
                assert isinstance(f, Feature), f"HasOne feature {f} does not inherit from FeaturesBase"
                if f.attribute_name == item:
                    return FeatureWrapper(self._chalk_feature.copy_with_path(f))
        raise AttributeError(item)


def unwrap_feature(maybe_feature_wrapper: Any) -> Feature:
    """Unwrap a class-annotated FeatureWrapper instance into the underlying feature.

    For example:

    .. code-block::

        @features
        class FooBar:
            foo: str
            bar: int

        type(FooBar.foo) is FeatureWrapper
        type(unwrap_feature(FooBar.foo)) is Feature
    """
    if isinstance(maybe_feature_wrapper, FeatureWrapper):
        return maybe_feature_wrapper._chalk_feature
    raise TypeError(f"{maybe_feature_wrapper} is of type {type(maybe_feature_wrapper)}, expecting type FeatureWrapper")


class Feature:
    def __init__(
        self,
        name: Optional[str] = None,
        attribute_name: Optional[str] = None,
        namespace: Optional[str] = None,
        features_cls: Optional[Type[Features]] = None,
        typ: Optional[Union[FeatureTypeAnnotation, type]] = None,
        version: Optional[int] = None,
        description: Optional[str] = None,
        owner: Optional[str] = None,
        tags: Optional[Tags] = None,
        primary: bool = False,
        max_staleness: Optional[Duration] = None,
        etl_offline_to_online: bool = False,
        encoder: Optional[Callable[[Any], JsonValue]] = None,
        decoder: Optional[Callable[[JsonValue], Any]] = None,
        join: Optional[Union[Callable[[], Filter], Filter]] = None,
        path: Tuple[HasOnePathObj, ...] = (),
        is_feature_time: bool = False,
    ):
        self.typ = FeatureTypeAnnotation(underlying=typ) if isinstance(typ, type) else typ
        self.features_cls = features_cls
        self.name = name
        self.attribute_name = attribute_name  # the attribute name for the feature in the @features class (in case if the name is specified differently)
        self.namespace = namespace
        self.path = path
        self.version = version
        self.description = description
        self.owner = owner
        self.tags = tags
        self.primary = primary
        self.max_staleness = max_staleness
        self.etl_offline_to_online = etl_offline_to_online
        self.encoder = encoder
        self.decoder = decoder
        self.is_feature_time = is_feature_time
        self._join = join

    def __str__(self):
        if len(self.path) > 0:
            return ".".join(
                [self.path[0].parent.namespace or "<unknown>"]
                + [(x.parent.name or "<unknown>") for x in self.path or []]
                + [self.name or "<unknown>"]
            )
        return f"{self.namespace}.{self.name}"

    def __repr__(self):
        return f"Feature(fqn={self.namespace}.{self.name}, typ={self.typ})"

    @property
    def fqn(self) -> str:
        return ".".join((x for x in [self.namespace, self.name] if isinstance(x, str)))

    @property
    def is_has_one(self):
        # A feature is a has-one relationship if the type is another singleton features cls and there is a join condition
        assert self.typ is not None
        # Need to short-circuit if it is a dataframe, as datafames might not have an underlying
        return not self.typ.is_dataframe and self.join is not None

    @property
    def is_has_many(self):
        assert self.typ is not None
        return self.typ.is_dataframe and self.join is not None

    @property
    def is_list(self):
        assert self.typ is not None
        return self.typ.is_list

    @property
    def has_resolved_join(self):
        return self._join is not None

    @property
    def join(self) -> Optional[Filter]:
        if self._join is not None:
            # Join was explicitly specified
            return self._join() if callable(self._join) else self._join
        # Attempt to extract the join condition from the foreign feature
        assert self.typ is not None
        foreign_features = self.typ.underlying
        if not issubclass(foreign_features, Features):
            return None
        assert self.features_cls is not None
        joins: List[Tuple[str, Filter]] = []  # Tuple of (name, Join)
        for f in foreign_features.features:
            assert isinstance(f, Feature)
            assert f.typ is not None
            if f.typ.underlying is self.features_cls and f.has_resolved_join:
                assert f.join is not None
                assert f.name is not None
                join = f.join() if callable(f.join) else f.join
                joins.append((f.name, join))
        if len(joins) == 0:
            # It's a nested feature
            return None
        # TODO(Ravi): Enable this check. But let's see if we can be smarter about which join to automatically use, if there are multiple
        # if len(joins) > 1:
        #     assert self.features_cls is not None
        #     raise ValueError(
        #         f"Multiple join conditions exist for {self.features_cls.__name__} and {foreign_features.__name__} on keys: "
        #         + f", ".join(f'{foreign_features.__name__}.{name}' for (name, _) in joins)
        #     )
        join = joins[0][1]
        if callable(join):
            join = join()
        self._join = join
        return join

    def copy_with_path(
        self,
        child: Feature,
    ):
        child_copy = copy.copy(child)
        assert child.attribute_name is not None
        child_copy.path = tuple(
            (
                *self.path,
                HasOnePathObj(
                    parent=self,
                    child=child,
                    parent_to_child_attribute_name=child.attribute_name,
                ),
            )
        )
        return child_copy


class Filter:
    def __init__(
        self,
        feature: Any,  # think of this as "LHS"
        operation: str,
        other: Any,  # think of this as "RHS", a feature or a constant
    ) -> None:
        # Feature or other could be another feature, filter, featuretime, literal
        # Other could also be a sequence (in the case of operation = "in")
        self.operation = operation
        if isinstance(feature, FeatureWrapper):
            feature = unwrap_feature(feature)
        self.feature = feature
        if self.operation == "in":
            if not isinstance(other, collections.abc.Iterable):
                raise ValueError("The RHS must be an iterable for operation='in'")
            other = {unwrap_feature(x) if isinstance(x, FeatureWrapper) else x for x in other}
        else:
            if isinstance(other, FeatureWrapper):
                other = unwrap_feature(other)
        self.other = other

    def __hash__(self) -> int:
        return hash((self.feature, self.operation, self.other))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Filter):
            return NotImplemented
        return self.feature == other.feature and self.operation == other.operation and self.other == other.other

    def __and__(self, other):
        return Filter(self, "and", other)

    def __or__(self, other):
        return Filter(self, "or", other)

    def __bool__(self):
        # If the operation is == or !=, then compare the underlying filters or features
        # If x and y are features, then (x == y) is overloaded to return a Filter
        # This allows bool(x == y) to return True iff the x is y, while (x == y) is still a Filter instance
        # Using identity instead of equality to prevent an infinite loop
        if self.operation == "==":
            return self.feature is self.other
        if self.operation == "!=":
            return self.feature is not self.other
        # Non-equality comparisons must be evaluated manually -- e.g. if x and y are Features
        # (x < y) would return a Filter, but bool(x < y) doesn't really make sense. So, raise.
        return NotImplemented

    def referenced_features(self) -> Set[Feature]:
        from chalk.parsed.feature import FeatureType

        result = set()
        if isinstance(self.feature, Feature):
            result.add(self.feature)

        if isinstance(self.other, Feature):
            result.add(self.other)
        if isinstance(self.feature, FeatureType):
            pass
        if isinstance(self.other, FeatureType):
            pass

        return result

    def __repr__(self):
        return f"Filter({self.feature} {self.operation} {self.other})"


class FeatureSetBase:
    """Registry containing all @features classes."""

    registry: Dict[str, Type[Features]] = {}  # mapping of fqn to Features cls

    def __init__(self) -> None:
        raise RuntimeError("FeatureSetBase should never be instantiated")


class FeaturesMeta(type):
    """Metaclass for classes decorated with ``@features``.

    This metaclass allows for:

    1.  Classes annotated with @features to pass the
        ``isinstance(x, Features)`` and ``issubclass(X, Features)`` checks.
    2.  ``Features[Feature1, Feature2]`` annotations to return subclasses of Features, so they can be used as proper type annotations.
    """

    def __subclasscheck__(self, subcls: type) -> bool:
        if not isinstance(subcls, type):
            raise TypeError(f"{subcls} is not a type")
        if hasattr(subcls, "__is_features__"):
            return getattr(subcls, "__is_features__")
        return False

    def __instancecheck__(self, instance: object) -> bool:
        return self.__subclasscheck__(type(instance))

    # This lets us subscript by the features
    def __getitem__(cls, item: Any) -> Type[Features]:
        from chalk.features.dataframe import DataFrame
        from chalk.parsed.feature import FeatureType

        # Typing the `__getitem__` as any, since the @features members are typed as the underlying data structure
        # But, they should always be features or a tuple of features
        if isinstance(item, type) and issubclass(item, Features):
            item = [f for f in item.features if isinstance(f, (Feature, FeatureWrapper))]
        item = ensure_tuple(item)
        item = tuple(x._chalk_feature if isinstance(x, FeatureWrapper) else x for x in item)
        for x in item:
            if isinstance(x, str):
                raise TypeError(
                    f'String features like {cls.__name__}["{x}"] are unsupported. Instead, replace with "{cls.__name__}[{x}]"'
                )
            if isinstance(x, (Feature, FeatureType)) or isinstance(x, type) and issubclass(x, DataFrame):
                continue

            raise TypeError(f"Invalid feature type: {x}")
        cls = cast(Type[Features], cls)

        new_features = tuple([*cls.features, *item])
        assert len(new_features) > 0

        class SubFeatures(cls):
            features = new_features

        return SubFeatures

    def __repr__(cls) -> str:
        cls = cast(Type[Features], cls)
        return f"Features[{', '.join(str(f) for f in cls.features)}]"

    @property
    def namespace(cls):
        cls = cast(Type[Features], cls)
        namespaces = [x.namespace for x in cls.features]
        return get_unique_item(namespaces, name=f"{cls.__name__} feature namespaces")


class Features(metaclass=FeaturesMeta):
    """Features base class.

    This class is rarely instantiated or directly inherited. However, classes
    annotated with @features can be thought of as inheriting from this class.
    It can be used with `isinstance()` and ``issubclass`` checks, as well as for
    typing.
    """

    # Internally, the Features class is instantiated when results come through, and
    # results are bound to instances of this class via attributes
    __chalk_primary__: ClassVar[Optional[Feature]]  # The primary key feature
    __chalk_ts__: ClassVar[Optional[Feature]]  # The timestamp feature
    features: Tuple[Union[Feature, FeatureType, Type[DataFrame]], ...] = ()
    __is_features__: bool = True

    # When constructing results, this class is instantiated


@dataclasses.dataclass
class TimeDelta:
    weeks_ago: int = 0
    days_ago: int = 0
    hours_ago: int = 0
    minutes_ago: int = 0
    seconds_ago: int = 0
    milliseconds_ago: int = 0
    microseconds_ago: int = 0

    def to_std(self) -> timedelta:
        # Returning the negative inverse since the feature is defined in the past (e.g. days **ago**)
        return -timedelta(
            weeks=self.weeks_ago,
            days=self.days_ago,
            hours=self.hours_ago,
            minutes=self.minutes_ago,
            seconds=self.seconds_ago,
            milliseconds=self.milliseconds_ago,
            microseconds=self.microseconds_ago,
        )


CHALK_TS_FEATURE = Feature(name="CHALK_TS", namespace="__chalk__", typ=datetime)
ChalkTime = CHALK_TS_FEATURE


def before(
    weeks_ago: int = 0,
    days_ago: int = 0,
    hours_ago: int = 0,
    minutes_ago: int = 0,
    seconds_ago: int = 0,
    milliseconds_ago: int = 0,
    microseconds_ago: int = 0,
) -> Any:
    return Filter(
        feature=CHALK_TS_FEATURE,
        operation="<=",
        other=TimeDelta(
            weeks_ago=weeks_ago,
            days_ago=days_ago,
            hours_ago=hours_ago,
            minutes_ago=minutes_ago,
            seconds_ago=seconds_ago,
            milliseconds_ago=milliseconds_ago,
            microseconds_ago=microseconds_ago,
        ),
    )


def after(
    weeks_ago: int = 0,
    days_ago: int = 0,
    hours_ago: int = 0,
    minutes_ago: int = 0,
    seconds_ago: int = 0,
    milliseconds_ago: int = 0,
    microseconds_ago: int = 0,
) -> Any:
    return Filter(
        feature=CHALK_TS_FEATURE,
        operation=">=",
        other=TimeDelta(
            weeks_ago=weeks_ago,
            days_ago=days_ago,
            hours_ago=hours_ago,
            minutes_ago=minutes_ago,
            seconds_ago=seconds_ago,
            milliseconds_ago=milliseconds_ago,
            microseconds_ago=microseconds_ago,
        ),
    )


UNPARSED_TIMESTAMP = Feature(typ=datetime)
