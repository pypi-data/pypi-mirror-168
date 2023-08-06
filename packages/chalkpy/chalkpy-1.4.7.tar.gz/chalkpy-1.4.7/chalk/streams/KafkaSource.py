from typing import List, Optional, TypeVar, Union

from pydantic import BaseModel

from chalk.streams.StreamSource import StreamSource


class KafkaConsumerConfig(BaseModel):
    broker: Union[str, List[str]]
    topic: Union[str, List[str]]
    ssl_keystore_location: Optional[str] = None
    client_id_prefix: Optional[str] = None
    group_id_prefix: Optional[str] = None
    topic_metadata_refresh_interval_ms: Optional[int] = None
    security_protocol: Optional[str] = None


T = TypeVar("T")


class KafkaSource(StreamSource[T]):
    def __init__(
        self,
        consumer_config: Optional[KafkaConsumerConfig] = None,
        message: Optional[T] = None,
    ):
        super(KafkaSource, self).__init__()
        self.Message = self
        self._message = message
        self.consumer_config = consumer_config
