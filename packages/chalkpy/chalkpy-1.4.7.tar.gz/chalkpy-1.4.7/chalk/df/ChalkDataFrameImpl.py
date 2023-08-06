import datetime
import enum
import functools
import logging
from typing import Any, Union

import pandas as pd

from chalk.features import Feature
from chalk.features.feature import FeatureWrapper, Filter, TimeDelta, unwrap_feature
from chalk.parsed.feature import FeatureTimeFeatureType, FeatureType

_logger = logging.getLogger(__name__)


def _feature_type_or_value(e):
    if isinstance(e, (Feature, FeatureWrapper)):
        return FeatureType.of(e)
    return e


class ChalkDataFrameImpl:
    def __init__(self, pandas_dataframe: pd.DataFrame):
        self.underlying = pandas_dataframe
        self.timestamp_feature = None
        for col in pandas_dataframe.columns:
            if isinstance(col, FeatureTimeFeatureType):
                if self.timestamp_feature is not None:
                    raise ValueError("DataFrame cannot have multiple timestamp features")
                self.timestamp_feature = col

    def _expect_scalar(self, v, name: str):
        if isinstance(v, pd.Series) and len(v) == 1:
            return v[0]
        if isinstance(v, pd.Series):
            raise ValueError(
                f"Cannot compute {name}. DataFrame contains {len(v)} features, and expected only one. "
                f"Filter your DataFrame down to the feature for which you want to compute the {name} "
                f"before calling .{name}()."
            )
        return v

    def mean(self):
        return self._expect_scalar(self.underlying.mean(), "mean")

    def median(self):
        return self._expect_scalar(self.underlying.median(), "median")

    def sum(self):
        return self._expect_scalar(self.underlying.sum(), "sum")

    def max(self):
        return self._expect_scalar(self.underlying.max(), "max")

    def min(self):
        return self._expect_scalar(self.underlying.min(), "min")

    def count(self) -> int:
        if isinstance(self.underlying, pd.DataFrame):
            return len(self.underlying)
        return self.underlying.count()

    def keys(self):
        return self.underlying.keys()

    def iterrows(self):
        return self.underlying.iterrows()

    @property
    def iloc(self):
        return self.underlying.iloc()

    def __repr__(self):
        return repr(self.underlying)

    def _maybe_replace_timestamp_feature(self, f: Union[Feature, Any]):
        """Replace the ``CHALK_TS`` pseudo-feature with the actual timestamp column."""
        if not isinstance(f, FeatureType) or f.fqn != "__chalk__.CHALK_TS":
            return f
        if self.timestamp_feature is None:
            raise ValueError("DataFrame has no timestamp")
        return self.timestamp_feature

    def _maybe_convert_timedelta_to_timestamp(
        self, f: Union[TimeDelta, datetime.timedelta, Any], now: datetime.datetime
    ):
        """Convert timedeltas relative to ``now`` into absolute datetimes."""
        if isinstance(f, TimeDelta):
            f = f.to_std()
        if isinstance(f, datetime.timedelta):
            return now + f
        return f

    def _parse_feature_or_value(self, f: Union[Feature, Any], now: datetime.datetime):
        """Parse a feature or value into the correct type that can be used for filtering."""
        f = _feature_type_or_value(f)
        f = self._maybe_convert_timedelta_to_timestamp(f, now)
        f = self._maybe_replace_timestamp_feature(f)
        if isinstance(f, enum.Enum):
            f = f.value
        return f

    def _get_filter(self, f: Filter, underlying: pd.DataFrame, now: datetime.datetime):
        """Evaluate a filter.

        Args:
            f (Filter): The filter.
            underlying (pd.DataFrame): The data frame.
            now (datetime.datetime): The datetime to use for the current timestamp. Used to resolve relative
                timestamps in filters to absolute datetimes.
        """
        # Passing `now` in explicitly instead of using datetime.datetime.now() so that multiple filters
        # relying on relative timestamps (e.g. before, after) will have the same "now" time.
        if f.operation == "not":
            return ~self._get_filter(f.feature, underlying, now)

        lhs = self._parse_feature_or_value(f.feature, now)
        rhs = self._parse_feature_or_value(f.other, now)

        if rhs is None and isinstance(lhs, FeatureType):
            if f.operation == "==":
                return underlying[lhs].isnull()

            elif f.operation == "!=":
                return underlying[lhs].notnull()

        if isinstance(lhs, FeatureType):
            lhs = underlying[lhs]

        if isinstance(rhs, FeatureType):
            rhs = underlying[rhs]

        if f.operation == "==":
            return lhs == rhs
        elif f.operation == "!=":
            return lhs != rhs
        elif f.operation == ">=":
            return lhs >= rhs
        elif f.operation == ">":
            return lhs > rhs
        elif f.operation == "<":
            return lhs < rhs
        elif f.operation == "<=":
            return lhs <= rhs
        elif f.operation == "in":
            return lhs.isin(rhs)
        elif f.operation == "not in":
            return ~lhs.isin(rhs)
        elif f.operation == "and":
            return self._get_filter(lhs, underlying, now) & self._get_filter(rhs, underlying, now)
        elif f.operation == "or":
            return self._get_filter(lhs, underlying, now) | self._get_filter(rhs, underlying, now)
        else:
            raise ValueError(f'Unknown operation "{f.operation}"')

    def __getitem__(self, item):
        try:
            from chalk.df.ChalkASTParser import ChalkASTParser

            item = ChalkASTParser.parse_dataframe_getitem(item)

            projections = []
            filters = []
            for x in item:
                if isinstance(x, FeatureWrapper):
                    x = unwrap_feature(x)
                if isinstance(x, Feature):
                    x = FeatureType.of(x)

                if isinstance(x, FeatureType):
                    projections.append(x)

                elif isinstance(x, Filter):
                    filters.append(x)

                else:
                    raise ValueError(f'Indexed chalk.DataFrame with invalid type "{type(item)}": {item}')
            underlying = self.underlying
            now = datetime.datetime.now()
            if len(filters) > 0:
                pandas_filters = [self._get_filter(f, underlying, now) for f in filters]
                single_filter = functools.reduce(lambda a, b: a & b, pandas_filters)
                underlying = underlying[single_filter]

            # Do the projection
            underlying = underlying[projections] if len(projections) > 0 else underlying

            return ChalkDataFrameImpl(underlying)

        except KeyError as e:
            _logger.debug(f"Failed to get key: {item}. Had keys: {self.underlying.keys()}", e)
            raise e

    @classmethod
    def from_pandas(cls, param):
        renames = {c: FeatureType.of(c) for c in param.columns}
        underlying = param.rename(columns=renames)
        return cls(underlying)

    def to_pandas(self) -> Union[pd.DataFrame, pd.Series]:
        renames = {c: str(c) for c in self.underlying.columns}
        return self.underlying.rename(columns=renames)
