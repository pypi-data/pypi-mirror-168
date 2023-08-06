import unittest
from datetime import datetime

from chalk.features import Features, feature_time, features, has_one, online


@features
class HomeFeatures:
    home_id: str
    address: str
    price: int
    sq_ft: int
    homeowner: "Homeowner" = has_one(lambda: Homeowner.home_id == HomeFeatures.home_id)


@features
class Homeowner:
    fullname: str
    home_id: str
    ts: datetime = feature_time()


@online
def get_home_data(
    hid: HomeFeatures.home_id, dd: HomeFeatures.homeowner.ts
) -> Features[HomeFeatures.price, HomeFeatures.sq_ft]:
    return HomeFeatures(
        price=200_000,
        sq_ft=2_000,
    )


class FeatureResolverCallableTestCase(unittest.TestCase):
    def test_multiple_output(self):
        pass


if __name__ == "__main__":
    unittest.main()
