from orm_base.table import TableBase
import pandas as pd

class SessionManager:

    def __init__(self, engine):
        self.engine = engine

    def __enter__(self):
        self.conn = self.engine.connect()
        return self.conn

    def __exit__(self, type, value, trace_back):
        self.conn.close()
        self.engine.dispose()


class QueryReader:

    def __init__(self, table: TableBase):
        self.table = self._check_type(table)
        self.columns = self.table.fields
        self._statement = self.table.statement

    def __str__(self):
        return str(self.table.statement)

    def __repr__(self):
        return repr(self.table.statement)

    @property
    def statement(self):
        return self._statement

    @statement.setter
    def statement(self, value):
        self._statement = value
        self.table.statement = value

    def _check_type(self, value):
        if not isinstance(value, TableBase):
            raise TypeError(f"table should be TableBase")
        return value

    def set_query(self, query):
        self.table.statement = query

    def read(self):
        with SessionManager(self.table.engine) as connection:
            exc = connection.execute(self.table.statement)
            result = exc.fetchall()
            self.table.reset_query()
        return result