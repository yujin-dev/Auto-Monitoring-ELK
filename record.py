from elasticsearch import Elasticsearch, helpers
from datetime import datetime
from sqlalchemy import create_engine,  select, column, table, text
from orm_base import QueryReader, TableBase
from config import *


class SessionLogger:

    _main_server = MAIN_ADDRESS
    _es_server = ES_ADDRESS

    def __init__(self):
        self.es = Elasticsearch(self._es_server)
        TARGET_SCHEMA.connect(create_engine(self._main_server))
        TARGET_SCHEMA.pg_stat_activity = TableBase("pg_stat_activity")
        self._table_reader = QueryReader(TARGET_SCHEMA.pg_stat_activity)

    def get_session(self):
        to_timestamp = lambda x: f"TO_CHAR({x}, 'YYYY-MM-DD HH24:MI:SS')" if x in ["query_start"] else x
        columns = ["pid", "client_addr", "query_start", "state"]
        self._table_reader.statement = text(f"select {','.join(list(map(to_timestamp, columns)))} from pg_stat_activity where state is not Null;")
        result = self._table_reader.read()
        result = [dict(zip(columns, res)) for res in result]
        return result

    def capture(self):
        current_session = self.get_session()
        self.bulk_insert(index="session_logger", data=current_session)

    def bulk_insert(self, index, data):
        def add_time(dt):
            dt["timestamp"] = datetime.now()
            return dt
        data = [{"_index": index, "_source": add_time(res)} for res in data]
        helpers.bulk(self.es, data)

    def search(self, index, query):
        result = self.es.search(index=index, body=query)
        return result


if __name__ == "__main__":

    slg = SessionLogger()
    slg.capture()