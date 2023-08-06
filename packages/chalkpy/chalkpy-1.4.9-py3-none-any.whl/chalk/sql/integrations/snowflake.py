from sqlalchemy.engine.url import URL

from chalk.sql.base.sql_source import BaseSQLSource


class SnowflakeSource(BaseSQLSource):
    def local_engine_url(self) -> URL:
        raise ValueError("Local Snowflake client not implemented")
