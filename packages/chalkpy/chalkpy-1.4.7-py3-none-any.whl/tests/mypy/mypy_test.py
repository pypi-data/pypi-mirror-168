from chalk.features.feature import Features
from chalk.features.feature_set import features


@features
class UserProfile:
    user_id: str
    profile_id: str
    address: int


@features
class Account:
    account_id: str
    balance: int


@features
class Transaction:
    user_id: str
    amount: int
    source_account_id: int
    dest_account_id: int


@features
class UserFeatures:
    uid: str
    name: str
    bday: str
    age: int


def name_age_good(
    age: UserFeatures.age,
) -> Features[UserFeatures.name, UserFeatures.age]:
    # Correctly knows that age is an int
    age_int_cast: int = age
    print(age_int_cast)
    # Correctly casts UserFeatures.__init__ to Features[name, age]
    return UserFeatures(name="4", age=4)


def name_age_good_flipped(
    age: UserFeatures.age,
) -> Features[UserFeatures.age, UserFeatures.name]:
    # Flips name and age to match
    return UserFeatures(name="4", age=4)


def name_age_bad() -> Features[UserFeatures.name, UserFeatures.age]:
    # We're getting Features[name, bday] and expected Features[name, age]
    return UserFeatures(name="4", bday="")


def name_bad_type() -> Features[UserFeatures.name]:
    # Knows that name should be a string, not an int
    return UserFeatures(name=4)
