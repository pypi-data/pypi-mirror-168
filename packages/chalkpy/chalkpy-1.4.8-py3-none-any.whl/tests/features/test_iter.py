import unittest
from datetime import datetime

from chalk.features import features, has_one
from chalk.features.feature_set import feature_time


@features
class NoFunFeatures:
    id: str


@features
class FunFeatures:
    id: str
    nope: str
    single_parent: "NoFunFeatures" = has_one(lambda: FunFeatures.nope == NoFunFeatures.id)
    ts = feature_time()


class BackPopulationOfFeaturesTestCase(unittest.TestCase):
    def test_features(self):
        now = datetime.now()
        self.assertDictEqual(
            {"fun_features.nope": "hello", "fun_features.ts": now},
            dict(FunFeatures(nope="hello", ts=now)),
        )
        self.assertDictEqual(
            {"fun_features.nope": "hello"},
            dict(FunFeatures(nope="hello")),
        )
        self.assertDictEqual(
            {"fun_features.nope": "hello"},
            dict(FunFeatures(nope="hello", single_parent=NoFunFeatures(id="a"))),
        )
        self.assertDictEqual({}, dict(FunFeatures()))


if __name__ == "__main__":
    unittest.main()
