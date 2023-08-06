from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel
from typing_extensions import Protocol


class StreamMessage(Protocol):
    value: Optional[Union[BaseModel, str]]
    key: Optional[str]
    topic: str
    timestamp: datetime
