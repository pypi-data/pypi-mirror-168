from chalk.sql.base.sql_source import BaseSQLSource


class InMemorySQLite(BaseSQLSource):
    def local_engine_url(self) -> str:
        return "sqlite:///:memory:?check_same_thread=true"


class FileSQLite(BaseSQLSource):
    def __init__(self, filename: str):
        self.filename = filename
        super(FileSQLite, self).__init__()

    def local_engine_url(self) -> str:
        return f"sqlite:///{self.filename}?check_same_thread=true"
