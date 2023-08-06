from typing import List, Mapping

import pandas as pd
from sqlalchemy.orm import Query as SqlAlchemyQuery

from chalk.features import Feature
from chalk.features.feature import Features
from chalk.parsed.feature import FeatureType


class ChalkSqlAlchemyQuery:
    _query: SqlAlchemyQuery
    _features: List[Feature]

    def __init__(self, features: List[Feature], query: SqlAlchemyQuery):
        self._query = query
        self._features = features

    def _updated(self, q: SqlAlchemyQuery):
        self._query = q
        return self

    def _all_as_result(self, tup):
        fqn_to_feature: Mapping[str, Feature] = {
            f.fqn: f for f in self._features if isinstance(f, (Feature, FeatureType))
        }
        fs = Features()
        fs.features = tuple(
            (fqn_to_feature[col_description["name"]] for col_description in self._query.column_descriptions)
        )
        if tup is not None:
            for (feat, value) in zip(fs.features, tup):
                setattr(fs, feat.name, value)
        else:
            raise ValueError("Failed to fetch any results from db")
        return fs

    def first(self):
        return self._all_as_result(self._query.first())

    def one_or_none(self):
        return self._all_as_result(self._query.one_or_none())

    def one(self):
        return self._all_as_result(self._query.one())

    def all(self):
        fqn_to_feature = {f.fqn: f for f in self._features if isinstance(f, (Feature, FeatureType))}
        tuples = self._query.all()
        return pd.DataFrame(
            tuples,
            columns=[fqn_to_feature[value["name"]] for value in self._query.column_descriptions],
        )

    def filter_by(self, **kwargs):
        return self._updated(self._query.filter_by(**kwargs))

    def filter(self, *criterion):
        return self._updated(self._query.filter(*criterion))

    def order_by(self, *clauses):
        return self._updated(self._query.order_by(*clauses))

    def group_by(self, *clauses):
        return self._updated(self._query.group_by(*clauses))

    def having(self, criterion):
        return self._updated(self._query.having(*criterion))

    def union(self, *q):
        return self._updated(self._query.union(*q))

    def union_all(self, *q):
        return self._updated(self._query.union_all(*q))

    def intersect(self, *q):
        return self._updated(self._query.intersect(*q))

    def intersect_all(self, *q):
        return self._updated(self._query.intersect_all(*q))

    def join(self, target, *props, **kwargs):
        return self._updated(self._query.join(target, *props, **kwargs))

    def outerjoin(self, target, *props, **kwargs):
        return self._updated(self._query.outerjoin(target, *props, **kwargs))

    def select_from(self, *from_obj):
        return self._updated(self._query.select_from(*from_obj))
