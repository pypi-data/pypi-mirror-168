from typing import Any, Callable, MutableMapping

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from chalk.sql.base.protocols import BaseSQLSourceProtocol, DBSessionMakerProtocol, DBSessionProtocol


class DBSession(DBSessionProtocol):
    def __init__(self, s: Session):
        self._session = s
        self._raw_session = s

    def update_query(self, f: Callable[[Session], Session]) -> None:
        self._session = f(self._session)

    def result(self) -> Any:
        return self._session

    def execute(self, q) -> Any:
        return self._session.execute(q)

    def close(self):
        return self._raw_session.close()


class DBSessionMaker(DBSessionMakerProtocol):
    def __init__(self):
        self._session_makers: MutableMapping[BaseSQLSourceProtocol, sessionmaker] = {}

    def get_session(self, source: BaseSQLSourceProtocol) -> DBSessionProtocol:
        if source not in self._session_makers:
            engine = create_engine(
                source.local_engine_url(),
                echo=False,
                **source.engine_args(),
            )
            sm: sessionmaker = sessionmaker(bind=engine)
            self._session_makers[source] = sm

        sm = self._session_makers[source]
        return DBSession(sm())
