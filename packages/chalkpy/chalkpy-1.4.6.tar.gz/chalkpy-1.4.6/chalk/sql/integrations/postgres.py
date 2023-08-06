from typing import Any, Mapping, Optional

from sqlalchemy.engine.url import URL

from chalk.integrations.named import load_integration_variable
from chalk.sql.base.sql_source import BaseSQLSource


class PostgreSQLSource(BaseSQLSource):
    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[str] = None,
        db: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        name: Optional[str] = None,
    ):
        self.host = host or load_integration_variable(integration_name=name, name="PGHOST")
        self.port = port or load_integration_variable(integration_name=name, name="PGPORT")
        self.db = db or load_integration_variable(integration_name=name, name="PGDATABASE")
        self.user = user or load_integration_variable(integration_name=name, name="PGUSER")
        self.password = password or load_integration_variable(integration_name=name, name="PGPASSWORD")

        super(PostgreSQLSource, self).__init__()

    def engine_args(self) -> Mapping[str, Any]:
        return dict(
            pool_size=20,
            max_overflow=60,
            # Trying to fix mysterious dead connection issue
            connect_args={
                "keepalives": 1,
                "keepalives_idle": 30,
                "keepalives_interval": 10,
                "keepalives_count": 5,
            },
        )

    def local_engine_url(self) -> str:
        return URL.create(
            drivername="postgresql",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.db,
        )
