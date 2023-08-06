import unittest
from datetime import datetime

from chalk.features import DataFrame, Feature, feature, feature_time, features, has_many, has_one
from chalk.features.feature import unwrap_feature


@features
class UnassignedIdFeatures:
    id: str
    other: str


@features
class UnassignedDecoratedIdFeatures:
    id: str = feature(owner="elliot@chalk.ai")
    other: str


@features
class OtherPrimaryKeyFeatures:
    id: str
    nah_really_this_is_id: str = feature(primary=True)
    other: str


@features
class ExplicitIdFeatures:
    id: str = feature(primary=True)
    other: str


@features
class BogusIdFeature1:
    id: str = has_one(lambda: ExplicitIdFeatures.id == BogusIdFeature1.other)
    other: str


@features
class BogusIdFeature2:
    id: DataFrame[ExplicitIdFeatures] = has_many(lambda: ExplicitIdFeatures.id == BogusIdFeature2.other)
    other: str


@features
class BogusIdFeature3:
    id: datetime = feature_time()
    other: str


@features
class IdIsNotIdFeatures:
    id: str = feature(name="not_id")
    other: str


@features
class NotIdIsIdFeatures:
    not_id: str = feature(name="id")
    other: str


class IdAssignmentTestCase(unittest.TestCase):
    def test_unassigned_assigned(self):
        self.assertTrue(unwrap_feature(UnassignedIdFeatures.id).primary)
        self.assertFalse(unwrap_feature(UnassignedIdFeatures.other).primary)
        self.assertEqual("id", UnassignedIdFeatures.__chalk_primary__.name)

    def test_unassigned_decorated_assigned(self):
        self.assertTrue(unwrap_feature(UnassignedDecoratedIdFeatures.id).primary)
        self.assertFalse(unwrap_feature(UnassignedDecoratedIdFeatures.other).primary)
        self.assertEqual("id", UnassignedDecoratedIdFeatures.__chalk_primary__.name)

    def test_other_primary_key(self):
        self.assertFalse(unwrap_feature(OtherPrimaryKeyFeatures.id).primary)
        self.assertTrue(unwrap_feature(OtherPrimaryKeyFeatures.nah_really_this_is_id).primary)
        self.assertEqual("nah_really_this_is_id", OtherPrimaryKeyFeatures.__chalk_primary__.name)

    def test_explicit_id(self):
        self.assertTrue(unwrap_feature(ExplicitIdFeatures.id).primary)
        self.assertFalse(unwrap_feature(ExplicitIdFeatures.other).primary)
        self.assertEqual("id", ExplicitIdFeatures.__chalk_primary__.name)

    def test_id_is_bogus(self):
        self.assertFalse(unwrap_feature(BogusIdFeature1.id).primary)
        self.assertIsNone(BogusIdFeature1.__chalk_primary__)

        self.assertFalse(unwrap_feature(BogusIdFeature2.id).primary)
        self.assertIsNone(BogusIdFeature2.__chalk_primary__)

        self.assertIsInstance(unwrap_feature(BogusIdFeature3.id), Feature)
        self.assertFalse(unwrap_feature(BogusIdFeature3.id).primary)
        self.assertIsNone(BogusIdFeature3.__chalk_primary__)

    def test_not_id_is_id(self):
        self.assertTrue(unwrap_feature(NotIdIsIdFeatures.not_id).primary)
        self.assertFalse(unwrap_feature(NotIdIsIdFeatures.other).primary)
        self.assertEqual("id", NotIdIsIdFeatures.__chalk_primary__.name)

    def test_id_is_not_id(self):
        self.assertFalse(unwrap_feature(IdIsNotIdFeatures.id).primary)
        self.assertFalse(unwrap_feature(IdIsNotIdFeatures.other).primary)
        self.assertIsNone(IdIsNotIdFeatures.__chalk_primary__)


if __name__ == "__main__":
    unittest.main()
