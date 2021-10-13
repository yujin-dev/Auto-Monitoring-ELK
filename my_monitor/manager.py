from my_monitor.record import SessionLogger


class SessionManager(SessionLogger):

    def kill_session(self, filter):
        query = "select pg_terminate_backend(pid) from pg_stat_activity where {};".format(filter)
        self.table.statement = query
        result = self.table.read()
        return result


    def kill_idle_session(self, minute=60):
        query = f"""
        select pg_terminate_backend(pid) from pg_stat_activity where state ('idle', 'idle in transaction', 'idle in transaction (aborted)', 'disabled') 
        and  client_addr not in ('127.0.0.1', '::1') 
        and current_timestamp - query_start > '{minute} min'; """
        self.table.statement = query
        result = self.table.read()
        return result