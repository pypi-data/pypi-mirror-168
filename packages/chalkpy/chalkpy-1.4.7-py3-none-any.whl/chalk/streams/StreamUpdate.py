from dataclasses import dataclass
from typing import List, Optional, Union

from chalk.features import Features


@dataclass
class StreamUpdate:
    online: Optional[Union[Features, List[Features]]] = None
    offline: Optional[Union[Features, List[Features]]] = None
