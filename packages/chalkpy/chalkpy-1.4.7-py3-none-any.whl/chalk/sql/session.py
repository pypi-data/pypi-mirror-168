from typing import List, Optional

from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy.orm import Session as SqlAlchemySession

from chalk.features import Feature, Features
from chalk.sql.query import ChalkSqlAlchemyQuery


class ChalkSqlAlchemySession:
    _session: Optional[SqlAlchemySession]

    def __init__(self, session: Optional[SqlAlchemySession]):
        self._session = session

    def set_session(self, s: SqlAlchemySession):
        self._session = s

    def query(self, *entities, **kwargs):
        if self._session is None:
            raise ValueError("Session needs to be set via chalk_session.set_session(...)")
        transformed_entities = []
        features: List[Feature] = []
        for e in entities:
            if isinstance(e, Features):
                for f in e.features:
                    features.append(f)
                    assert f.name is not None, "The name should be defined"
                    instrumented_attribute = getattr(e, f.name)
                    if isinstance(instrumented_attribute, InstrumentedAttribute):
                        transformed_entities.append(instrumented_attribute.label(f.fqn))
            else:
                raise ValueError("Values need to be wrapped")

        return ChalkSqlAlchemyQuery(features, self._session.query(*transformed_entities, **kwargs))
