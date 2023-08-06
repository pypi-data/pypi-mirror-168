import sys
import logging
from typing import Dict, List, Optional
from pandas import DataFrame

import snowflake.connector
from snowflake.connector.errors import ProgrammingError

from .database import Database
from .file_format import FileFormat
from .role import Role
from .schema import Schema
from .stage import Stage
from .storage_integration import StorageIntegration
from .warehouse import Warehouse


class SnowflakeConnector:
    """
    Driver for Snowflake Data Warehouse. Enables to connect to the SF account and execute queries.
    There is no need to log in and use Worksheets. Connection instance is enough to run any command.
    Basic drill recommendation:
        - `snowflake.connect()` - to connect to the account with given credentials
        - `snowflake.set_environment()` - to set up SF working environment for the whole session
        - `snowflake.execute()` or `snowflake.query_pd()` - to run any command you want
            (and eventually get the results in a nice Pandas DataFrame)
    For more information, please refer to functions' documentation.
    Moreover, there are 2 extra session's objects accessible: `cursor` and `connection` that are raw
        `snowflake-python-connector` objects. If you need, you can refer to Snowflake docs and perform extra tasks that
        aren't (yet) implemented in this driver.
    If the functionality you're looking for is not implemented yet, please create an issue in
        (naas-drivers repository)[https://github.com/jupyter-naas/drivers/tree/main],
        we would be more than happy to help.
    """

    def __init__(
        self,
        account: str,
        username: str,
        password: str,
        warehouse: str = "",
        database: str = "",
        schema: str = "",
        role: str = "",
    ):
        """
        Connects to Snowflake account with given credentials.
        Connection is established and both `connection` and `cursor` are being set up
        :param account: SF account identifier, can be fetched from login URL,
            e.g. <account_identifier>.snowflakecomputing.com
        :param username: SF account username
        :param password: SF account password
        :param warehouse: SF warehouse to set up while creating a connection
        :param database: SF database to set up while creating a connection
        :param schema: SF schema to set up while creating a connection
        :param role: SF role to set up while creating a connection
        """

        self._connection = snowflake.connector.connect(account=account, user=username, password=password)
        self._cursor = self._connection.cursor()
        self.set_environment(warehouse, database, schema, role)

        # Creating Snowflake objects
        self._database = Database(self)
        self._file_format = FileFormat(self)
        self._role = Role(self)
        self._schema = Schema(self)
        self._stage = Stage(self)
        self._storage_integration = StorageIntegration(self)
        self._warehouse = Warehouse(self)

    @property
    def connection(self):
        return self._connection

    @property
    def cursor(self):
        return self._cursor

    @property
    def database(self):
        return self._database

    @property
    def file_format(self):
        return self._file_format

    @property
    def role(self):
        return self._role

    @property
    def schema(self):
        return self._schema

    @property
    def stage(self):
        return self._stage

    @property
    def storage_integration(self):
        return self._storage_integration

    @property
    def warehouse(self):
        return self._warehouse

    def execute(self, sql: str, n: int = 10, silent: bool = False) -> Optional[Dict]:
        """
        Execute passed command. Could be anything, starting from DQL query, and ending with DDL commands
        :param sql: command/query to execute
        :param n: query result length limit
        :param silent: whether to return result dictionary with multiple information or not (run in silent mode)
        :return dictionary containing query information outcome (results, columns_metadata, and sql statement)
        """
        res = self._cursor.execute(sql)

        if silent:
            return None
        else:
            return {
                "results": res.fetchall() if n == -1 else res.fetchmany(n),
                "description": res.description,
                "statement": sql,
            }

    def query_pd(self, sql: str, n: int = 10) -> DataFrame:
        """
        Query data and return results in the form of pandas.DataFrame
        :param sql: query to execute
        :param n: query result length limit
        :return pandas.DataFrame table containing query outcome
        """
        res = self.execute(sql, n)

        # TODO: Apply dtypes mapping from ResultMetadata objects
        return DataFrame(
            res["results"],
            columns=[result_metadata.name for result_metadata in res["description"]],
        )

    def copy_into(
        self,
        table_name: str,
        source_stage: str,
        transformed_columns: str = "",
        files: List[str] = None,
        regex_pattern: str = "",
        file_format_name: str = "",
        validation_mode: str = "",
        silent: bool = False,
        **kwargs,
    ) -> Optional[Dict]:
        """
        Copy data from stage to Snowflake table
        As this function contains a lot of nuances, please refer to the documentation:
            https://docs.snowflake.com/en/sql-reference/sql/copy-into-table.html
        :param table_name: the name of the table into which data is loaded. Optionally, can specify namespace too
            (i.e., <database_name>.<schema_name> or <schema_name> if database is already selected)
        :param source_stage: internal or external location where the files containing data to be loaded are staged
            caution: it can be also a SELECT statement so data from stage is transformed
        :param transformed_columns: if `source_stage` is a SELECT statement,
            specifies an explicit set of fields/columns (separated by commas) to load from the staged data files
        :param files: a list of one or more files names (in an array) to be loaded
        :param regex_pattern: a regular expression pattern for filtering files from the output
        :param file_format_name: the format of the data files to load (so far only name is accepted as an input)
        :param validation_mode: instructs the COPY command to validate the data files
            instead of loading them into the specified table.
            Caution: does not support COPY statements that transform data during a load.
            If applied along with transformation SELECT statement, it will throw error on Snowflake side
        :param silent: whether to run in silent mode (see `SnowflakeConnector.execute()`)
        :return result dictionary (see: `SnowflakeConnector.execute()`)
        """
        statement = "COPY INTO" f" {table_name}"

        # If applicable, then data load with transformation has been scheduled
        # If not, it's a standard data load
        if source_stage.upper().strip().startswith("SELECT"):
            statement += f"{' ' + transformed_columns if transformed_columns != '' else ''}" f" FROM ({source_stage})"
        else:
            statement += f" FROM {source_stage}"

        files_string = ",".join([f"'{file}'" for file in files]) if files is not None else ""
        statement += f"{f' ({files_string})' if files_string != '' else ''}"

        statement += (
            f"{f' PATTERN = {regex_pattern}' if regex_pattern != '' else ''}"
            f"{f' FILE FORMAT = (FORMAT_NAME = {file_format_name})' if file_format_name != '' else ''}"
            f"{f' VALIDATION_MODE = {validation_mode}' if validation_mode != '' else ''}"
        )

        # looping through kwargs for extra arguments passed in statement
        # while executing final command, Snowflake will do the validation
        for key, value in kwargs.items():
            statement += f" {key} = {value}"

        return self.execute(statement, n=1, silent=silent)

    def close_connection(self) -> None:
        """
        Closes a connection to Snowflake account, resets all the internal parameters
        """
        self._cursor.close()
        self._connection.close()

        self._cursor = None
        self._connection = None

    def get_environment(self) -> Dict:
        """
        Returns current session environment that consists of:
            - role
            - database
            - schema
            - warehouse
        :return dictionary of current session environment elements
        """

        return {
            "role": self._role.get_current(),
            "database": self._database.get_current(),
            "schema": self._schema.get_current(),
            "warehouse": self._warehouse.get_current(),
        }

    def set_environment(self, warehouse: str = "", database: str = "", schema: str = "", role: str = "") -> None:
        """
        Tries to set Snowflake environment in bulk: warehouse, database, schema, and role
        :param warehouse: warehouse to set in the environment
        :param database: database to set in the environment
        :param schema: schema to set in the environment
        :param role: role to set in the environment
        """
        warehouse, database, schema, role = (
            warehouse.strip(),
            database.strip(),
            schema.strip(),
            role.strip(),
        )
        try:
            if warehouse != "":
                self._warehouse.use(warehouse)
            if database != "":
                self._database.use(database)
            if schema != "":
                self._schema.use(schema)
            if role != "":
                self._role.use(role)
        except ProgrammingError as pe:
            logging.error(f"Error while setting SF environment. More on that: {pe}")
            sys.exit()
