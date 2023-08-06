import dataclasses
import enum
from datetime import date, datetime, timezone
from typing import Any, Dict, Optional

import cattrs
import numpy as np
import pandas
import pendulum
import pydantic
import pytz
from dateutil import parser

from chalk.features import Feature, FeatureSetBase
from chalk.features.feature import Features
from chalk.utils.enum import get_enum_value_type

try:
    import attrs
except ImportError:
    # Imports not available. Attrs is not required.
    attrs = None


class FeatureCodec:
    def __init__(
        self,
        fqn_to_feature: Optional[Dict[str, Feature]] = None,
    ):
        self._fqn_to_feature = (
            fqn_to_feature
            if fqn_to_feature is not None
            else {
                feature.fqn: feature
                for fsb in FeatureSetBase.registry.values()
                for feature in fsb.features
                if isinstance(feature, Feature)
            }
        )
        self.converter = cattrs.Converter()
        self.converter.register_structure_hook(datetime, lambda v, _: parser.isoparse(v))
        self.converter.register_unstructure_hook(
            datetime, lambda v: (v if v.tzinfo else pytz.utc.localize(v)).isoformat()
        )

    def _default_encode(self, value: Any, for_pandas: bool = False):
        if isinstance(value, list):
            return [self._default_encode(x) for x in value]
        if isinstance(value, (str, int, float)):
            return value
        if isinstance(value, enum.Enum):
            return self._default_encode(value.value)
        if isinstance(value, datetime):
            tz = value.tzinfo or (datetime.now(timezone.utc).astimezone().tzinfo)
            return pendulum.instance(value, tz).isoformat()
        if isinstance(value, date):
            return value.isoformat()
        if isinstance(value, np.integer):
            return int(value)
        if isinstance(value, np.floating):
            return float(value)
        if isinstance(value, pandas.Timestamp):
            return pendulum.instance(value.to_pydatetime()).isoformat()
        if isinstance(value, pydantic.BaseModel):
            return value.dict()
        if (attrs is not None and attrs.has(type(value))) or dataclasses.is_dataclass(value):
            return self.converter.unstructure(value)
        raise TypeError(f"Unable to encode value of type {type(value).__name__}")

    def encode(
        self,
        feature: Feature,
        value: Any,
    ):
        if value is None:
            return None

        if feature.encoder is not None:
            return feature.encoder(value)

        return self._default_encode(value)

    def encode_fqn(self, fqn: str, value: Any):
        if fqn in self._fqn_to_feature:
            return self.encode(self._fqn_to_feature[fqn], value)

        return self._default_encode(value)

    def _default_decode_value(
        self,
        feature: Feature,
        value: Any,
    ):
        assert feature.typ is not None
        if issubclass(feature.typ.underlying, enum.Enum):
            value = feature.typ.underlying(value)
        if issubclass(feature.typ.underlying, datetime):
            value = parser.isoparse(value)
        elif issubclass(feature.typ.underlying, date):
            # note: datetime is a subclass of date, so we must be careful to decode accordingly
            value = date.fromisoformat(value)
        if issubclass(feature.typ.underlying, pydantic.BaseModel):
            return feature.typ.underlying(**value)
        elif (attrs is not None and attrs.has(feature.typ.underlying)) or dataclasses.is_dataclass(
            feature.typ.underlying
        ):
            return self.converter.structure(value, feature.typ.underlying)
        if not isinstance(value, feature.typ.underlying):
            raise TypeError(f"Unable to decode value {value} to type {feature.typ.underlying.__name__}")
        return value

    def _default_decode(
        self,
        feature: Feature,
        value: Any,
    ):
        assert feature.typ is not None
        if value is None:
            if feature.typ.is_nullable:
                return None
            else:
                raise ValueError(f"Value is none but feature {feature} is not nullable")
        if feature.typ.is_list:
            if not isinstance(value, list):
                raise TypeError(f"Feature {feature} is a list but value {value} is not")
            return [self._default_decode_value(feature, x) for x in value]
        else:
            return self._default_decode_value(feature, value)

    def decode(
        self,
        feature: Feature,
        value: Any,
    ):
        if value is None:
            return None

        if feature.decoder is not None:
            return feature.decoder(value)

        return self._default_decode(feature, value)

    def decode_fqn(
        self,
        fqn: str,
        value: Any,
    ):
        if fqn in self._fqn_to_feature:
            return self.decode(self._fqn_to_feature[fqn], value)
        return value

    def get_dtype(self, fqn: str) -> str:
        feature = self._fqn_to_feature[fqn]
        typ = feature.typ
        assert typ is not None, "typ should be specified"
        underlying = typ.underlying
        if issubclass(underlying, enum.Enum):
            # For enums, require all members to have the same type
            underlying = get_enum_value_type(underlying)
            assert underlying is not None, "enums should have at least one member"
        # See https://pandas.pydata.org/docs/user_guide/basics.html#basics-dtypes
        if issubclass(underlying, str):
            return "object"
        if issubclass(underlying, bool):
            return "boolean"
        if issubclass(underlying, int):
            return "Int64"
        if issubclass(underlying, float):
            return "Float64"
        if issubclass(underlying, datetime):
            return "object"
        if issubclass(underlying, date):
            return "object"
        if issubclass(underlying, Features):
            return "object"
        raise TypeError(f"Unsupported type: {underlying.__name__}")
