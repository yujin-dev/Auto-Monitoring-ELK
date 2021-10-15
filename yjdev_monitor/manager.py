from datetime import datetime
from yjdev_monitor.sql_table import TableManager
import pandas as pd


class SessionManager:

    def __init__(self, server_address, alias=None):
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
        return [self.revise(res) for res in result]

    def session_callback(self, func):
        current_session = self.get_session(filter="state is not Null")
        return func(data=current_session)

    def revise(self, dt):
        dt["timestamp"] = self.now
        dt["query_start"] = pd.to_datetime(dt["query_start"])
        dt["alias"] = self.alias
        return dt

    def kill_session(self, filter):
        query = "select pg_terminate_backend(pid) from pg_stat_activity where {};".format(filter)
        self.table.statement = query
        result = self.table.read()
        return result

    def kill_idle_session(self, minute=60):
        query = f"""
        select pg_terminate_backend(pid) from pg_stat_activity where state in ('idle', 'idle in transaction', 'idle in transaction (aborted)', 'disabled') 
        and  client_addr not in ('127.0.0.1', '::1') 
        and current_timestamp - query_start > '{minute} min'; """
        self.table.statement = query
        result = self.table.read()
        return result