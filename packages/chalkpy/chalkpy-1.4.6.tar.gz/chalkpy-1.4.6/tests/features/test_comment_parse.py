import unittest
from datetime import datetime

from chalk.features import feature, feature_time, features
from chalk.features.feature import unwrap_feature


@features(tags="t", owner="andy@chalk.ai")
class WowFS:
    # This is a really neat description of something
    something: str

    # This is also really neat and cool
    something_else: str
    nocomment: str

    nope: str

    assigned: str = feature(tags="a")

    # bizarre
    bizarre: str

    # goofy
    goofy: str = feature(owner="yo")

    # now with feature
    assigned_comment: str = feature(tags=["3", "4"])

    # implicit comment
    explicit: str = feature(description="explicit comment")

    # Multiline
    # Neat and, verily, cool
    #
    # Hello
    assigned_comment_multiline: str = feature()

    # now with feature time
    time: datetime = feature_time()

    nope_nope: datetime  # Datetime field that is not feature time


@features(owner="elliot@chalk.ai")
class OwnerFeatures:
    plain: str
    cached: str = feature(max_staleness="3d")
    andy: str = feature(owner="andy@chalk.ai")

    ft: datetime = feature_time()


@features(tags=["1", "2"])
class TagFeatures:
    empty: str
    one: str = feature(tags="one")
    many: str = feature(tags=["a", "b"])

    ft: datetime = feature_time()


class ParseCommentsTestCase(unittest.TestCase):
    def test_parse_descriptions(self):
        self.assertEqual("bizarre", unwrap_feature(WowFS.bizarre).description)
        self.assertEqual(
            "This is a really neat description of something",
            unwrap_feature(WowFS.something).description,
        )
        self.assertEqual("explicit comment", unwrap_feature(WowFS.explicit).description)
        self.assertEqual(
            "This is also really neat and cool",
            unwrap_feature(WowFS.something_else).description,
        )
        self.assertEqual("now with feature", unwrap_feature(WowFS.assigned_comment).description)
        self.assertEqual("goofy", unwrap_feature(WowFS.goofy).description)
        self.assertEqual(
            """Multiline
Neat and, verily, cool

Hello""",
            unwrap_feature(WowFS.assigned_comment_multiline).description,
        )

    def test_class_owner(self):
        self.assertEqual("elliot@chalk.ai", OwnerFeatures.__chalk_owner__)
        self.assertEqual("elliot@chalk.ai", unwrap_feature(OwnerFeatures.plain).owner)
        self.assertEqual("elliot@chalk.ai", unwrap_feature(OwnerFeatures.cached).owner)
        self.assertEqual("andy@chalk.ai", unwrap_feature(OwnerFeatures.andy).owner)

    def test_class_tags(self):
        self.assertEqual(["1", "2"], TagFeatures.__chalk_tags__)
        self.assertEqual(["1", "2"], unwrap_feature(TagFeatures.empty).tags)
        self.assertEqual(["one", "1", "2"], unwrap_feature(TagFeatures.one).tags)
        self.assertEqual(["a", "b", "1", "2"], unwrap_feature(TagFeatures.many).tags)
        self.assertEqual(["a", "t"], unwrap_feature(WowFS.assigned).tags)
        self.assertEqual(["t"], unwrap_feature(WowFS.nope).tags)
        self.assertEqual(["3", "4", "t"], unwrap_feature(WowFS.assigned_comment).tags)


if __name__ == "__main__":
    unittest.main()
