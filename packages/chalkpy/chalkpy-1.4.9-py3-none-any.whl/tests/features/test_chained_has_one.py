import unittest

from chalk.features import features, has_one
from chalk.features.feature import HasOnePathObj, unwrap_feature


@features
class ExampleFraudOrg:
    uid: str
    org_name: str


@features
class ExampleFraudUser:
    uid: str
    org: ExampleFraudOrg = has_one(lambda: ExampleFraudUser.uid == ExampleFraudOrg.uid)


@features
class ExampleFraudProfile:
    uid: str
    user: ExampleFraudUser = has_one(lambda: ExampleFraudProfile.uid == ExampleFraudUser.uid)


class ChainedHasOneTestCase(unittest.TestCase):
    def test_chain(self):
        referenced_org = unwrap_feature(ExampleFraudProfile.user.org.org_name)

        self.assertEqual(len(referenced_org.path), 2)
        self.assertIsInstance(referenced_org.path[0], HasOnePathObj)
        self.assertIsInstance(referenced_org.path[1], HasOnePathObj)


if __name__ == "__main__":
    unittest.main()
