import tempfile
import unittest

import pandas as pd
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from chalk.df.ChalkDataFrameImpl import ChalkDataFrameImpl
from chalk.features import features
from chalk.features.feature import Features
from chalk.parsed.feature import FeatureType
from chalk.sql.base.protocols import IncrementalSettings
from chalk.sql.integrations.sqlite import FileSQLite

Base = declarative_base()


class UserTable(Base):
    __tablename__ = "users_testing"
    id = Column(String, primary_key=True)
    name = Column(String)
    email = Column(String)


class AccountsTable(Base):
    __tablename__ = "accounts_testing"
    id = Column(String, primary_key=True)
    user_id = Column(String)
    title = Column(String)


@features
class UserFeatures:
    id: str
    name: str
    email: str


@features
class AccountFeatures:
    id: str
    user_id: str
    title: str


tmp = tempfile.NamedTemporaryFile(delete=False)
db = FileSQLite(tmp.name)
# db = PostgreSQLSource()


class SQLBaseTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        engine = create_engine(db.local_engine_url())
        s = sessionmaker(bind=engine)()
        UserTable.__table__.create(engine)
        AccountsTable.__table__.create(engine)

        s.add_all(
            [
                UserTable(id="u_2", name="elliot", email="elliot@chalk.ai"),
                UserTable(id="u_3", name="andy", email="andy@chalk.ai"),
                UserTable(id="u_4", name="marc", email="marc@chalk.ai"),
                AccountsTable(id="a_1", user_id="u_2", title="elliot marx"),
                AccountsTable(id="a_2", user_id="u_2", title="elliot r marx"),
            ]
        )
        s.commit()

    def test_query_all(self):
        query = (
            db.query(UserFeatures(id=UserTable.id, name=UserTable.name, email=UserTable.email))
            .filter_by(name="elliot")
            .all()
        )
        self.assertIsNone(query._incremental_settings)
        result = query.execute()
        self.assertIsInstance(result, ChalkDataFrameImpl)

    def test_query_all_incremental(self):
        query = (
            db.query(UserFeatures(id=UserTable.id, name=UserTable.name, email=UserTable.email))
            .filter_by(name="elliot")
            .all(incremental=True)
        )
        self.assertEqual(
            query._incremental_settings,
            IncrementalSettings(lookback_period=None),
        )
        result = query.execute()
        self.assertIsInstance(result, ChalkDataFrameImpl)

    def test_query_all_incremental_lookback(self):
        query = (
            db.query(UserFeatures(id=UserTable.id, name=UserTable.name, email=UserTable.email))
            .filter_by(name="elliot")
            .all(incremental=IncrementalSettings(lookback_period="1d"))
        )
        self.assertEqual(
            query._incremental_settings,
            IncrementalSettings(lookback_period="1d"),
        )
        result = query.execute()
        self.assertIsInstance(result, ChalkDataFrameImpl)

    def test_query_one(self):
        query = (
            db.query(UserFeatures(id=UserTable.id, name=UserTable.name, email=UserTable.email))
            .filter_by(name="elliot")
            .one()
        )
        result = query.execute()
        assert isinstance(result, Features)
        self.assertIsNotNone(result)
        self.assertEqual(result.email, "elliot@chalk.ai")
        self.assertEqual(result.name, "elliot")
        self.assertEqual(result.id, "u_2")

    def test_query_string_one(self):
        base_query = db.query_string(
            query="select id, email from users_testing where name=:n",
            fields=dict(email=UserFeatures.email, id=UserFeatures.id),
            args=dict(n="elliot"),
        )
        result = base_query.one().execute()
        assert isinstance(result, Features)
        self.assertEqual(result.email, "elliot@chalk.ai")
        self.assertEqual(result.id, "u_2")

    def test_query_string_all(self):
        query = db.query_string(
            query="select id, email from users_testing where name=:n",
            fields=dict(email=UserFeatures.email, id=UserFeatures.id),
            args=dict(n="elliot"),
        ).all()
        self.assertIsNone(query._incremental_settings)
        result = query.execute()
        self.assertIsInstance(result, ChalkDataFrameImpl)

    def test_query_string_all_incremental_lookback(self):
        query = db.query_string(
            query="select id, email from users_testing where name=:n",
            fields=dict(email=UserFeatures.email, id=UserFeatures.id),
            args=dict(n="elliot"),
        ).all(incremental=IncrementalSettings(lookback_period="1d"))
        self.assertEqual(
            query._incremental_settings,
            IncrementalSettings(lookback_period="1d"),
        )
        result = query.execute()
        self.assertIsInstance(result, ChalkDataFrameImpl)

    def test_query_string_all_incremental(self):
        base_query = db.query_string(
            query="select id, email from users_testing where name=:n",
            fields=dict(email=UserFeatures.email, id=UserFeatures.id),
            args=dict(n="elliot"),
        ).all(incremental=True)
        self.assertEqual(
            base_query._incremental_settings,
            IncrementalSettings(lookback_period=None),
        )
        result = base_query.execute()
        self.assertIsInstance(result, ChalkDataFrameImpl)

    def test_join(self):
        query = (
            db.query(
                AccountFeatures(
                    title=AccountsTable.title,
                    user_id=AccountsTable.user_id,
                    id=AccountsTable.id,
                )
            )
            .join(UserTable, UserTable.id == AccountsTable.user_id)
            .filter(UserTable.id == "u_2")
        )
        result = query.execute()
        pd.testing.assert_frame_equal(
            result.underlying,
            pd.DataFrame(
                data=[
                    ["a_1", "u_2", "elliot marx"],
                    ["a_2", "u_2", "elliot r marx"],
                ],
                columns=[
                    FeatureType.of(AccountFeatures.id),
                    FeatureType.of(AccountFeatures.user_id),
                    FeatureType.of(AccountFeatures.title),
                ],
            ),
        )
