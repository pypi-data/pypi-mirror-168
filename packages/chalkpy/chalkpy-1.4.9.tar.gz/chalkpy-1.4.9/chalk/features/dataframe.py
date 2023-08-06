from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, Iterable, List, Mapping, Optional, Tuple, Type, Union, cast

import pandas as pd

from chalk.utils.collections import ensure_tuple, get_unique_item

if TYPE_CHECKING:
    from chalk.features.feature import Feature, Features, Filter


class DataFrameMeta(type):
    def __getitem__(cls, item) -> Type[DataFrame]:
        # leaving untyped as we type the individual features as their object type
        # but item should really be filter (expressions), Feature classes, or Feature instances
        from chalk.df.ChalkASTParser import ChalkASTParser
        from chalk.features.feature import Feature, Features, FeatureWrapper, Filter

        cls = cast(Type[DataFrame], cls)

        item = ensure_tuple(item)

        # Disallow string annotations like DataFrame["User"].
        # Instead, the entire thing should be in quotes -- like "DataFrame[User]"
        for x in item:
            if isinstance(x, str):
                raise TypeError(
                    f'Annotation {cls.__name__}["{x}", ...] is unsupported. Instead, use a string for the entire annotation -- for example: '
                    f'"{cls.__name__}[{x}, ...]"'
                )

        # If doing multiple subscript, then keep the filters, but do not keep the individual columns
        # TODO: Validate that any new columns are a subset of the existing columns
        item = [*item, *cls.filters]

        item = ChalkASTParser.parse_dataframe_getitem(item)

        new_filters: List[Filter] = []
        new_references_feature_set: Optional[Type[Features]] = None
        new_columns: List[Feature] = []

        for a in item:
            if isinstance(a, Filter):
                new_filters.append(a)
            elif isinstance(a, type) and issubclass(a, Features):
                if new_references_feature_set is not None:
                    raise ValueError(
                        f"Multiple referenced feature sets -- {new_references_feature_set} and {a} -- are not supported."
                    )
                new_references_feature_set = a
            elif isinstance(a, Feature):
                new_columns.append(a)
            elif isinstance(a, FeatureWrapper):
                new_columns.append(a._chalk_feature)
            else:
                raise TypeError(f"Invalid type for DataFrame[{a}]: {type(a)}")

        if len(new_columns) == 0 and new_references_feature_set is None:
            # This is possible if you have something like
            # Users.transactions[after('60d')]
            # In this case, keep all existing columns
            # But if you did
            # Users.transactions[Transaction.id, after('60d')]
            # Then keep only the id column
            new_columns = list(cls.columns)

        class SubclassedDataFrame(cls):
            filters = tuple(new_filters)
            __columns__ = tuple(new_columns)
            references_feature_set = new_references_feature_set

        return SubclassedDataFrame

    def __call__(cls, *args: None, **kwargs: None):
        # Allowing args and kwargs to display our custom error message below
        raise RuntimeError("DataFrame(...) should never be instantiated. Use DataFrame[...] notation instead.")

    def __repr__(cls):
        cls = cast(Type[DataFrame], cls)
        elements = [str(x) for x in (*cls.filters, *cls.columns)]
        if cls.references_feature_set is not None:
            elements.append(cls.references_feature_set.__name__)
        return f"DataFrame[{', '.join(elements)}]"

    def __instancecheck__(self, other: object) -> bool:
        raise RuntimeError(
            "DataFrame cannot be used with an isinstance(x, DataFrame) check. Instead, use issubclass(x, DataFame)."
        )

    @property
    def columns(cls) -> Tuple[Feature, ...]:
        # Computing the columns lazily as we need to implicitly parse the type annotation
        # to determine if a field is a has-many, and we don't want to do that on the
        # __getitem__ which could happen before forward references can be resolved
        # So, using a property on the metaclass, which acts like an attribute on the class, to
        # provide the dataframe columns
        from chalk.features.feature import Feature

        cls = cast(Type[DataFrame], cls)
        columns: List[Feature] = []
        for x in cls.__columns__:
            if not x.is_has_many:
                columns.append(x)
        if cls.references_feature_set is not None:
            for x in cls.references_feature_set.features:
                assert isinstance(x, Feature)
                if not x.is_has_many and not x.is_has_one:
                    columns.append(x)

        return tuple(columns)

    @property
    def namespace(cls) -> str:
        cls = cast(Type[DataFrame], cls)
        namespaces = [x.path[0].parent.namespace if len(x.path) > 0 else x.namespace for x in cls.columns]
        return get_unique_item(namespaces, f"dataframe {cls.__name__} column namespaces")


class DataFrame(metaclass=DataFrameMeta):
    filters: Tuple[Filter, ...] = ()
    columns: Tuple[Feature, ...]  # set via a decorator on the metaclass
    __columns__: Tuple[Feature, ...] = ()
    references_feature_set: Optional[Type[Features]] = None

    @classmethod
    def from_dict(cls, d: Dict[Any, List[Any]]):
        from chalk.df.ChalkDataFrameImpl import ChalkDataFrameImpl
        from chalk.parsed.feature import FeatureType

        return ChalkDataFrameImpl.from_pandas(pd.DataFrame({FeatureType.of(k): v for k, v in d.items()}))

    @classmethod
    def from_list(cls, *args: Union[List[Any], Any]):
        from chalk.features.feature import Features

        def _yield_args(a):
            if isinstance(a, Features):
                yield a

            elif isinstance(a, Iterable):
                for aa in a:
                    yield from _yield_args(aa)

            else:
                raise ValueError("Items in list must be wrapped in a feature set")

        from_dict = defaultdict(list)
        keys_frozen = False
        for arg in _yield_args(args):
            arg_dict = dict(arg)
            if keys_frozen and arg_dict.keys() != from_dict.keys():
                raise ValueError(
                    f"DataFrame.from_list received objects with different sets of features:"
                    f" {set(arg_dict.keys())} vs {set(from_dict.keys())}"
                )

            for k, v in arg_dict.items():
                from_dict[k].append(v)

            keys_frozen = True

        return cls.from_dict(from_dict)

    @classmethod
    def from_pandas(
        cls,
        df: pd.DataFrame,
    ):
        from chalk.df.ChalkDataFrameImpl import ChalkDataFrameImpl

        return ChalkDataFrameImpl.from_pandas(df)

    @classmethod
    def read_parquet(
        cls,
        path: Union[str, Path],
        columns: Union[Mapping[str, Any], Mapping[int, Any]],
    ):
        from chalk.df.ChalkDataFrameImpl import ChalkDataFrameImpl
        from chalk.parsed.feature import FeatureType

        return ChalkDataFrameImpl.from_pandas(
            pd.read_parquet(
                path=path,
                columns=list(columns.keys()),
            ).rename(columns={k: FeatureType.of(v) for k, v in columns.items()})
        )

    @classmethod
    def read_csv(
        cls,
        path: Union[str, Path],
        columns: Union[Mapping[str, Any], Mapping[int, Any]],
    ):
        from chalk.df.ChalkDataFrameImpl import ChalkDataFrameImpl
        from chalk.parsed.feature import FeatureType

        return ChalkDataFrameImpl.from_pandas(
            pd.read_csv(filepath_or_buffer=path).rename(columns={k: FeatureType.of(v) for k, v in columns.items()})
        )
