import unittest

from pydantic import BaseModel

from chalk.features import features
from chalk.streams import KafkaSource, stream
from chalk.streams.StreamUpdate import StreamUpdate


@features
class StreamFeatures:
    scalar_feature: str


class KafkaMessage(BaseModel):
    val_a: str


s = KafkaSource(message=KafkaMessage)


@stream
def fn(message: s.Message):
    return StreamUpdate(
        online=StreamFeatures(
            scalar_feature=message.val_a,
        )
    )


class StreamTestCase(unittest.TestCase):
    def test_callable(self):
        self.assertEqual(
            fn(KafkaMessage(val_a="hello")),
            StreamUpdate(online=StreamFeatures(scalar_feature="hello")),
        )

    def test_parsed_source(self):
        self.assertEqual(fn.source, s)
