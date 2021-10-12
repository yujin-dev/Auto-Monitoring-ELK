import pandas as pd
from elasticsearch import Elasticsearch, helpers
from datetime import datetime
from my_monitor.sql_table import TableManager


class SessionLogger:

    _es_server = "http://localhost:9200/"

    def __init__(self, server_address, alias=None):
        self.es = Elasticsearch(self._es_server)
        self.table = TableManager("pg_stat_activity")
        self.table.connect(server_address)
        self.alias = alias
        self.now = datetime.now()

    def get_session(self, filter: str = None):
        to_timestamp = lambda x: f"TO_CHAR({x}, 'YYYY-MM-DD HH24:MI:SS')" if x in ["query_start"] else x
        columns = ["pid", "client_addr", "query_start", "state", "state_change"]
        query = f"select {','.join(list(map(to_timestamp, columns)))} from pg_stat_activity"
        if filter:
            query += f" where {filter}"
        self.table.statement = query
        result = self.table.read()
        result = [dict(zip(columns, res)) for res in result]
        return result

    def capture(self):
        current_session = self.get_session(filter="state is not Null")
        self.insert_session(data=current_session)

    def insert_session(self, data):
        def revise(dt):
            dt["timestamp"] = self.now
            dt["query_start"] = pd.to_datetime(dt["query_start"])
            dt["alias"] = self.alias
            return dt
        data = [{"_index": "session_logger", "_source": revise(res)} for res in data]
        helpers.bulk(self.es, data)

    def search(self, index, query):
        result = self.es.search(index=index, body=query)
        return result