import enum
import unittest
from datetime import date

import pandas

from chalk.client import _ChalkAPIClientImpl
from chalk.client.client_impl import _OfflineQueryResponse
from chalk.features.feature import Feature
from chalk.serialization.codec import FeatureCodec


class Gender(enum.Enum):
    M = "m"
    F = "f"
    X = "x"


class TestClientSerialization(unittest.TestCase):
    def test_deserialize_null_int_enum(self):
        client = _ChalkAPIClientImpl(
            client_id="dummy",
            client_secret="dummy",
            environment="dummy",
            api_server="dummy",
        )

        client._codec = FeatureCodec(
            fqn_to_feature={
                "user.id": Feature(name="id", namespace="user", typ=int),
                "user.gender": Feature(name="gender", namespace="user", typ=Gender),
            }
        )

        fixture_response = _OfflineQueryResponse(
            columns=["user.id", "user.gender"],
            output=[
                [1, None],
                ["m", "f"],
            ],
        )

        # this shouldn't throw
        client._decode_offline_response(offline_query_response=fixture_response)

    def test_deserialize_date(self):
        client = _ChalkAPIClientImpl(
            client_id="dummy",
            client_secret="dummy",
            environment="dummy",
            api_server="dummy",
        )

        client._codec = FeatureCodec(
            fqn_to_feature={"user.birthday": Feature(name="birthday", namespace="user", typ=date)}
        )

        fixture_response = _OfflineQueryResponse(
            columns=["user.birthday"],
            output=[
                ["2022-09-08"],
            ],
        )

        decoded_frame = client._decode_offline_response(offline_query_response=fixture_response)
        pandas.testing.assert_frame_equal(
            decoded_frame,
            pandas.DataFrame(data={"user.birthday": [date.fromisoformat("2022-09-08")]}),
        )
