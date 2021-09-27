from sqlalchemy import MetaData, Table, Column


class TableBase:
    metadata = MetaData()

    def __init__(self, table_name):
        self.name = table_name
        self._statement = None
        self.engine = None
        self.base = None

    @property
    def target(self):
        if self.engine is None:
            raise ConnectionError(f"Table {self.name} should be connect to engine")
        return self.base

    @property
    def fields(self):
        return self.target.c.keys()

    @property
    def statement(self):
        return self._statement

    @statement.setter
    def statement(self, value):
        self._statement = value

    def connect(self, engine):
        self.engine = engine
        self.base = Table(self.name, self.metadata, autoload_with=self.engine)

    def reset_query(self):
        self.statement = None