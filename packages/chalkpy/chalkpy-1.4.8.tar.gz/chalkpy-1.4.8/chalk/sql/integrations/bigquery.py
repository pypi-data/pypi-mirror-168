from sqlalchemy.engine.url import URL

from chalk.sql.base.sql_source import BaseSQLSource


class BigQuerySource(BaseSQLSource):
    def local_engine_url(self) -> URL:
        raise NotImplemented("Local BigQuery client not implemented")
