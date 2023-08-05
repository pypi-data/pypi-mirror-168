# Copyright 2022 Cloudera Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from contextlib import contextmanager
from dataclasses import dataclass

import time
import dbt.exceptions

from dbt.adapters.base import Credentials
from dbt.adapters.sql import SQLConnectionManager
from dbt.contracts.connection import AdapterRequiredConfig

from typing import Optional, Tuple, Any

from dbt.contracts.connection import Connection, AdapterResponse, ConnectionState

from dbt.events.functions import fire_event
from dbt.events.types import ConnectionUsed, SQLQuery, SQLQueryStatus

from dbt.logger import GLOBAL_LOGGER as LOGGER

import impala.dbapi

import dbt.adapters.impala.__version__ as ver
import dbt.adapters.impala.cloudera_tracking as tracker

import json

DEFAULT_IMPALA_HOST = "localhost"
DEFAULT_IMPALA_PORT = 21050
DEFAULT_MAX_RETRIES = 3


@dataclass
class ImpalaCredentials(Credentials):
    host: str = DEFAULT_IMPALA_HOST
    schema: str = None
    database: Optional[str] = None
    port: Optional[int] = DEFAULT_IMPALA_PORT
    username: Optional[str] = None
    password: Optional[str] = None
    auth_type: Optional[str] = None
    kerberos_service_name: Optional[str] = None
    use_http_transport: Optional[bool] = True
    use_ssl: Optional[bool] = True
    http_path: Optional[str] = ""  # for supporting a knox proxy in ldap env
    usage_tracking: Optional[bool] = True  # usage tracking is enabled by default
    retries: Optional[int] = DEFAULT_MAX_RETRIES

    _ALIASES = {"dbname": "database", "pass": "password", "user": "username"}

    @classmethod
    def __pre_deserialize__(cls, data):
        data = super().__pre_deserialize__(data)
        if "database" not in data:
            data["database"] = None
        return data

    def __post_init__(self):
        # impala classifies database and schema as the same thing
        if self.database is not None and self.database != self.schema:
            raise dbt.exceptions.RuntimeException(
                f"    schema: {self.schema} \n"
                f"    database: {self.database} \n"
                f"On Impala, database must be omitted or have the same value as"
                f" schema."
            )
        self.database = None

        # set the usage tracking flag
        tracker.usage_tracking = self.usage_tracking
        # get platform information for tracking
        tracker.populate_platform_info(self, ver)
        # generate unique ids for tracking
        tracker.populate_unique_ids(self)

    @property
    def type(self):
        return "impala"

    def _connection_keys(self):
        # return an iterator of keys to pretty-print in 'dbt debug'.
        # Omit fields like 'password'!
        return "host", "port", "schema", "username"

    @property
    def unique_field(self) -> str:
        # adapter anonymous adoption
        return self.host


class ImpalaConnectionManager(SQLConnectionManager):
    TYPE = "impala"

    def __init__(self, profile: AdapterRequiredConfig):
        super().__init__(profile)
        # generate profile related object for instrumentation.
        tracker.generate_profile_info(self)

    @contextmanager
    def exception_handler(self, sql: str):
        try:
            yield
        except impala.dbapi.DatabaseError as exc:
            LOGGER.debug("dbt-impala error: {}".format(str(exc)))
            raise dbt.exceptions.DatabaseException(str(exc))
        except Exception as exc:
            LOGGER.debug("Error running SQL: {}".format(sql))
            raise dbt.exceptions.RuntimeException(str(exc))

    @classmethod
    def open(cls, connection):
        if connection.state == ConnectionState.OPEN:
            LOGGER.debug("Connection is already open, skipping open.")
            return connection

        credentials = connection.credentials
        connection_ex = None

        auth_type = "insecure"

        try:
            connection_start_time = time.time()
            # the underlying dbapi supports retries, so this is directly used instead to support retries
            if (
                    credentials.auth_type == "LDAP" or credentials.auth_type == "ldap"
            ):  # ldap connection
                handle = impala.dbapi.connect(
                    host=credentials.host,
                    port=credentials.port,
                    auth_mechanism="LDAP",
                    use_http_transport=credentials.use_http_transport,
                    user=credentials.username,
                    password=credentials.password,
                    use_ssl=credentials.use_ssl,
                    http_path=credentials.http_path,
                    retries=credentials.retries,
                )
                auth_type = "ldap"
            elif (
                    credentials.auth_type == "GSSAPI"
                    or credentials.auth_type == "gssapi"
                    or credentials.auth_type == "kerberos"
            ):  # kerberos based connection
                handle = impala.dbapi.connect(
                    host=credentials.host,
                    port=credentials.port,
                    auth_mechanism="GSSAPI",
                    kerberos_service_name=credentials.kerberos_service_name,
                    use_http_transport=credentials.use_http_transport,
                    use_ssl=credentials.use_ssl,
                    retries=credentials.retries,
                )
                auth_type = "kerberos"
            else:  # default, insecure connection
                handle = impala.dbapi.connect(
                    host=credentials.host,
                    port=credentials.port,
                    retries=credentials.retries,
                )
            connection_end_time = time.time()

            connection.state = ConnectionState.OPEN
            connection.handle = handle
        except Exception as ex:
            LOGGER.debug("Connection error {}".format(ex))
            connection_ex = ex
            connection.state = ConnectionState.FAIL
            connection.handle = None
            connection_end_time = time.time()

        # track usage
        payload = {
            "event_type": "dbt_impala_open",
            "auth": auth_type,
            "connection_state": connection.state,
            "elapsed_time": "{:.2f}".format(
                connection_end_time - connection_start_time
            ),
        }

        if connection.state == ConnectionState.FAIL:
            payload["connection_exception"] = "{}".format(connection_ex)

        tracker.track_usage(payload)

        return connection

    @classmethod
    def close(cls, connection):
        try:
            # if the connection is in closed or init, there's nothing to do
            if connection.state in {ConnectionState.CLOSED, ConnectionState.INIT}:
                return connection

            connection_close_start_time = time.time()
            connection = super().close(connection)
            connection_close_end_time = time.time()

            payload = {
                "event_type": "dbt_impala_close",
                "connection_state": ConnectionState.CLOSED,
                "elapsed_time": "{:.2f}".format(
                    connection_close_end_time - connection_close_start_time
                ),
            }

            tracker.track_usage(payload)

            return connection
        except Exception as err:
            LOGGER.debug(f"Error closing connection {err}")

    @classmethod
    def get_response(cls, cursor):
        message = "OK"
        return AdapterResponse(_message=message)

    def cancel(self, connection):
        connection.handle.close()

    def add_begin_query(self, *args, **kwargs):
        LOGGER.debug("NotImplemented: add_begin_query")

    def add_commit_query(self, *args, **kwargs):
        LOGGER.debug("NotImplemented: add_commit_query")

    def commit(self, *args, **kwargs):
        LOGGER.debug("NotImplemented: commit")

    def rollback(self, *args, **kwargs):
        LOGGER.debug("NotImplemented: rollback")

    def add_query(
            self,
            sql: str,
            auto_begin: bool = True,
            bindings: Optional[Any] = None,
            abridge_sql_log: bool = False,
    ) -> Tuple[Connection, Any]:
        connection = self.get_thread_connection()
        if auto_begin and connection.transaction_open is False:
            self.begin()
        fire_event(ConnectionUsed(conn_type=self.TYPE, conn_name=connection.name))

        additional_info = {}
        if self.query_header:
            try:
                additional_info = json.loads(self.query_header.comment.query_comment.strip())
            except Exception as ex:  # silently ignore error for parsing
                additional_info = {}
                LOGGER.debug(f"Unable to get query header {ex}")

        with self.exception_handler(sql):
            if abridge_sql_log:
                log_sql = "{}...".format(sql[:512])
            else:
                log_sql = sql

            # track usage
            payload = {
                "event_type": "dbt_impala_start_query",
                "sql": log_sql,
                "profile_name": self.profile.profile_name
            }

            for key, value in additional_info.items():
                payload[key] = value

            tracker.track_usage(payload)

            fire_event(SQLQuery(conn_name=connection.name, sql=log_sql))
            pre = time.time()

            cursor = connection.handle.cursor()

            # paramstyle parameter is needed for the datetime object to be correctly quoted when
            # running substitution query from impyla. this fix also depends on a patch for impyla:
            # https://github.com/cloudera/impyla/pull/486
            configuration = {"paramstyle": "format"}
            query_exception = None
            try:
                cursor.execute(sql, bindings, configuration)
                query_status = str(self.get_response(cursor))
            except Exception as ex:
                query_status = str(ex)
                query_exception = ex

            elapsed_time = time.time() - pre

            payload = {
                "event_type": "dbt_impala_end_query",
                "sql": log_sql,
                "elapsed_time": "{:.2f}".format(elapsed_time),
                "status": query_status,
                "profile_name": self.profile.profile_name
            }

            tracker.track_usage(payload)

            # re-raise query exception so that it propogates to dbt
            if (query_exception):
                raise query_exception

            fire_event(
                SQLQueryStatus(
                    status=query_status,
                    elapsed=round(elapsed_time, 2),
                )
            )

            return connection, cursor
