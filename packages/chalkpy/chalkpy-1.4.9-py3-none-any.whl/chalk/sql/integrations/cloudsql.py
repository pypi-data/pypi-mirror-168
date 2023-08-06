import logging
import os
from typing import Any, Mapping, Optional

from sqlalchemy.engine.url import URL

from chalk.sql.base.sql_source import BaseSQLSource

_logger = logging.getLogger(__name__)


class CloudSQLSource(BaseSQLSource):
    def __init__(
        self,
        instance_name: Optional[str] = None,
        db: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        name: Optional[str] = None,
    ):
        prefix = name + "_" if name else ""
        self.instance_name = instance_name or os.getenv(prefix + "CLOUDSQL_INSTANCE_NAME")
        self.db = db or os.getenv(prefix + "CLOUDSQL_DATABASE")
        self.user = user or os.getenv(prefix + "CLOUDSQL_USER")
        self.password = password or os.getenv(prefix + "CLOUDSQL_PASSWORD")

        super(CloudSQLSource, self).__init__()

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
        _logger.debug(f"Connecting to CloudSQL instance {self.instance_name}")
        return URL.create(
            drivername="postgresql",
            username=self.user,
            password=self.password,
            host="",
            query={"host": "{}/{}/.s.PGSQL.5432".format("/cloudsql", self.instance_name)},
            database=self.db,
        )
