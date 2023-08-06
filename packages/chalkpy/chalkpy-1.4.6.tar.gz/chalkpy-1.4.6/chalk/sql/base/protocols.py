from typing import Any, Callable, Mapping, Optional, Protocol, Union

from pydantic import BaseModel
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import Session

from chalk.features import Feature
from chalk.utils.duration import Duration


class IncrementalSettings(BaseModel):
    lookback_period: Optional[Duration]


class StringChalkQueryProtocol(Protocol):
    def execute(self):
        ...

    def one_or_none(self):
        ...

    def one(self):
        ...

    def all(self, incremental: Union[bool, IncrementalSettings] = False):
        ...


class ChalkQueryProtocol(Protocol):
    def first(self) -> "ChalkQueryProtocol":
        ...

    def one_or_none(self) -> "ChalkQueryProtocol":
        ...

    def one(self) -> Any:
        ...

    def all(self, incremental: Union[bool, IncrementalSettings] = False) -> Any:
        ...

    def filter_by(self, **kwargs) -> "ChalkQueryProtocol":
        ...

    def filter(self, *criterion) -> "ChalkQueryProtocol":
        ...

    def order_by(self, *clauses) -> "ChalkQueryProtocol":
        ...

    def group_by(self, *clauses) -> "ChalkQueryProtocol":
        ...

    def having(self, criterion) -> "ChalkQueryProtocol":
        ...

    def union(self, *q) -> "ChalkQueryProtocol":
        ...

    def union_all(self, *q) -> "ChalkQueryProtocol":
        ...

    def intersect(self, *q) -> "ChalkQueryProtocol":
        ...

    def intersect_all(self, *q) -> "ChalkQueryProtocol":
        ...

    def join(self, target, *props, **kwargs) -> "ChalkQueryProtocol":
        ...

    def outerjoin(self, target, *props, **kwargs) -> "ChalkQueryProtocol":
        ...

    def select_from(self, *from_obj) -> "ChalkQueryProtocol":
        ...

    def execute(self):
        ...


class DBSessionProtocol(Protocol):
    def update_query(self, f: Callable[[Session], Session]) -> None:
        ...

    def result(self) -> Any:
        ...

    def execute(self, q) -> Any:
        ...

    def close(self):
        ...


class DBSessionMakerProtocol(Protocol):
    def get_session(self, source: "BaseSQLSourceProtocol") -> DBSessionProtocol:
        ...


class BaseSQLSourceProtocol(Protocol):
    def query_string(
        self,
        query: str,
        fields: Mapping[str, Feature],
        args: Optional[Mapping[str, str]],
    ) -> StringChalkQueryProtocol:
        ...

    def query(self, *entities, **kwargs) -> ChalkQueryProtocol:
        ...

    def local_engine_url(self) -> Union[str, URL]:
        ...

    def set_session_maker(self, maker: DBSessionMakerProtocol) -> None:
        ...

    def engine_args(self) -> Mapping[str, Any]:
        return {}
