import enum
import unittest
from datetime import date, datetime

import pendulum

from chalk.features import Feature, feature, features
from chalk.features.feature import unwrap_feature
from chalk.serialization.codec import FeatureCodec


class CustomClass:
    def __init__(self, w: str):
        self.w = w

    def __eq__(self, other):
        return isinstance(other, CustomClass) and self.w == other.w


class Gender(enum.Enum):
    M = "m"
    F = "f"
    X = "x"


@features
class Hello:
    a: str
    b: int
    c: datetime
    d: Gender
    e: date
    fancy: CustomClass = feature(encoder=lambda x: x.w, decoder=lambda x: CustomClass(x))


class FeatureCodecTestCase(unittest.TestCase):
    codec = FeatureCodec()

    def _check_roundtrip(self, f: Feature, value):
        encoded = self.codec.encode(f, value)
        decoded = self.codec.decode(f, encoded)
        self.assertTrue(decoded == value)

    def test_datetime(self):
        serialized = "2022-04-08T22:26:03.303000+00:00"
        decoded = self.codec.decode(unwrap_feature(Hello.c), serialized)
        self.assertEqual(decoded, pendulum.parse(serialized))
        re_encoded = self.codec.encode(unwrap_feature(Hello.c), decoded)
        self.assertEqual(serialized, re_encoded)

    def test_custom_codecs(self):
        self._check_roundtrip(unwrap_feature(Hello.fancy), CustomClass("hihi"))

    def test_gender(self):
        self._check_roundtrip(unwrap_feature(Hello.d), Gender.F)

    def test_date(self):
        self.assertEqual(
            "2022-04-08",
            self.codec.encode(unwrap_feature(Hello.e), date.fromisoformat("2022-04-08")),
        )
        self._check_roundtrip(unwrap_feature(Hello.e), date.fromisoformat("2022-04-08"))
