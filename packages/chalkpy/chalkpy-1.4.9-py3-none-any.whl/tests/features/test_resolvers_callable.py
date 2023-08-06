import unittest

from chalk.features import Features, features, online


@features
class HomeFeatures:
    home_id: str
    address: str
    price: int
    sq_ft: int


@online
def get_address(
    hid: HomeFeatures.home_id,
) -> HomeFeatures.address:
    return "Bridge Street" if hid == 1 else "Filbert Street"


@online
def get_home_data(
    hid: HomeFeatures.home_id,
) -> Features[HomeFeatures.price, HomeFeatures.sq_ft]:
    return HomeFeatures(
        price=200_000,
        sq_ft=2_000,
    )


class FeatureResolverCallableTestCase(unittest.TestCase):
    def test_single_output(self):
        self.assertEqual(
            get_address(2),
            "Filbert Street",
        )

    def test_multiple_output(self):
        result = get_home_data(2)
        self.assertEqual(result.price, 200_000)
        self.assertEqual(result.sq_ft, 2_000)

        self.assertNotEqual(
            result,
            HomeFeatures(
                address="hello",
                price=200_000,
                sq_ft=2_000,
            ),
        )

        self.assertEqual(
            result,
            HomeFeatures(
                price=200_000,
                sq_ft=2_000,
            ),
        )


if __name__ == "__main__":
    unittest.main()
