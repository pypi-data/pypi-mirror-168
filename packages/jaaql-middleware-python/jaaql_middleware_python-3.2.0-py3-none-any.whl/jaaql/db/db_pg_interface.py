from psycopg import OperationalError
from psycopg_pool import ConnectionPool
from psycopg.errors import ProgrammingError

import traceback

from jaaql.db.db_interface import DBInterface, ECHO__none, CHAR__newline
from jaaql.exceptions.http_status_exception import *
from jaaql.exceptions.custom_http_status import CustomHTTPStatus

ERR__connect_db = "Could not create connection to database!"

PGCONN__min_conns = 5
PGCONN__max_conns = 1
PGCONN__max_conns_jaaql_user = 10

ALLOWABLE_COMMANDS = ["SELECT ", "INSERT ", "UPDATE ", "DELETE "]

ERR__command_not_allowed = "Command not allowed. Please use one of " + str(ALLOWABLE_COMMANDS)


class DBPGInterface(DBInterface):

    HOST_POOLS = {}

    def __init__(self, config, host: str, port: int, db_name: str, username: str, role: str = None, password: str = None):
        super().__init__(config, host, username)

        self.role = role

        self.output_query_exceptions = config["DEBUG"]["output_query_exceptions"].lower() == "true"
        self.username = username
        self.db_name = db_name

        if self.username not in DBPGInterface.HOST_POOLS:
            DBPGInterface.HOST_POOLS[self.username] = {}

        user_pool = DBPGInterface.HOST_POOLS[self.username]

        if password is not None:
            try:
                conn_str = "user=" + username + " password=" + password + " dbname=" + db_name
                # Important we don't list the host as this will force a unix socket
                if host is not None and host not in ['localhost', '127.0.0.1']:
                    conn_str += " host=" + host

                if str(port) != "5432":
                    conn_str += " port=" + str(port)

                if self.db_name not in user_pool:
                    user_pool[self.db_name] = ConnectionPool(conn_str, min_size=PGCONN__min_conns, max_size=PGCONN__max_conns_jaaql_user,
                                                             max_lifetime=60 * 30)
            except OperationalError as ex:
                if "does not exist" in str(ex).split("\"")[-1]:
                    raise HttpStatusException(str(ex), CustomHTTPStatus.DATABASE_NO_EXIST)
                else:
                    raise HttpStatusException(str(ex))

        self.pg_pool = user_pool[self.db_name]

    def get_conn(self):
        try:
            conn = self.pg_pool.getconn()
            if self.role is not None:
                with conn.cursor() as cursor:
                    cursor.execute("SET SESSION AUTHORIZATION '" + self.role + "';")
                    conn.commit()

        except Exception as ex:
            traceback.print_exc()
            raise HttpStatusException(ERR__connect_db, HTTPStatus.INTERNAL_SERVER_ERROR)

        return conn

    def put_conn(self, conn):
        if self.role is not None:
            with conn.cursor() as cursor:
                cursor.execute("RESET SESSION AUTHORIZATION;")

        return self.pg_pool.putconn(conn)

    def close(self):
        DBPGInterface.HOST_POOLS[self.username].pop(self.db_name)
        self.pg_pool.close()

    def execute_query(self, conn, query, parameters=None):
        while True:
            try:
                with conn.cursor() as cursor:
                    do_prepare = False

                    if self.role is not None:
                        do_prepare = True
                        if not any([query.upper().startswith(ok_command) for ok_command in ALLOWABLE_COMMANDS]):
                            raise HttpStatusException(ERR__command_not_allowed)

                    if parameters is None or len(parameters.keys()) == 0:
                        cursor.execute(query, prepare=do_prepare)
                    else:
                        cursor.execute(query, parameters, prepare=do_prepare)
                    if cursor.description is None:
                        return [], []
                    else:
                        return [desc[0] for desc in cursor.description], cursor.fetchall()
            except OperationalError as ex:
                if ex.sqlstate is not None and ex.sqlstate.startswith("08"):
                    traceback.print_exc()
                    self.pg_pool.putconn(conn)
                    self.pg_pool.check()
                    conn = self.get_conn()
                else:
                    if self.output_query_exceptions:
                        traceback.print_exc()
                    raise ex
            except Exception as ex:
                if self.output_query_exceptions:
                    traceback.print_exc()
                raise ex

    def commit(self, conn):
        conn.commit()

    def rollback(self, conn):
        conn.rollback()

    def handle_db_error(self, err, echo):
        if isinstance(err, ProgrammingError):
            err = err.pgresult.error_message.decode("ASCII")

        err = str(err)
        if echo != ECHO__none:
            err += CHAR__newline + echo
        raise HttpStatusException(err, HTTPStatus.BAD_REQUEST)
