from chalk.features.feature import Features
from chalk.features.feature_set import features


@features
class UserFeatures:
    name: str
    bday: str
    age: int


def name_age_bad() -> Features[UserFeatures.name, UserFeatures.age]:
    # We're getting Features[name, bday] and expected Features[name, age]
    return UserFeatures(name="4", bday="")


def name_age_good_flipped() -> Features[UserFeatures.age, UserFeatures.name]:
    # Flips name and age to match
    return UserFeatures(name="4", age=4)


def name_bad_type() -> Features[UserFeatures.name]:
    # Knows that name should be a string, not an int
    UserFeatures(what=4)
    return UserFeatures(name=4)
