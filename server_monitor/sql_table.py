import sqlalchemy.exc
from sqlalchemy import MetaData, Table, create_engine

class SessionManager:

    def __init__(self, engine):
        self.engine = engine

    def __enter__(self):
        self.conn = self.engine.connect()
        return self.conn

    def __exit__(self, type, value, trace_back):
        self.conn.close()
        self.engine.dispose()


class ServerException:
    pass


class TableManager:
    metadata = MetaData()

    def __init__(self, table_name):
        self.name = table_name
        self.engine = None
        self._table = None
        self._statement = None

    @property
    def target(self):
        if self.engine is None:
            raise ConnectionError(f"Table {self.name} should be connect to engine")
        return self._table

    @property
    def fields(self):
        return self.target.c.keys()

    @property
    def statement(self):
        return self._statement

    @statement.setter
    def statement(self, value):
        self._statement = value

    def connect(self, db_address):
        self.engine = create_engine(db_address)
        self._table = Table(self.name, self.metadata, autoload_with=self.engine)

    def reset_query(self):
        self.statement = None

    def set_query(self, query):
        self.statement = query

    def read(self):
        if self.engine is None:
            raise ConnectionError(f"Table {self.name} should be connect to engine")
        try:
            with SessionManager(self.engine) as connection:
                exc = connection.execute(self.statement)
                result = exc.fetchall()
                self.reset_query()
            return result
        except sqlalchemy.exc.SQLAlchemyError as e:
            return e