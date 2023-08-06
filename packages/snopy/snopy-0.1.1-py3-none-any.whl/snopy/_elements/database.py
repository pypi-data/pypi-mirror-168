from typing import Dict, List, Optional


class Database:
    def __init__(self, snowflake_connector):
        self.__snowflake_connector = snowflake_connector

    def use(self, database_name: str, silent: bool = False) -> Optional[Dict]:
        """
        Sets particular database for a session
        :param database_name: name of the database to use
        :param silent: whether to run in silent mode (see `SnowflakeConnector.execute()`)
        :return result dictionary (see: `SnowflakeConnector.execute()`)
        """
        statement = "USE" f" DATABASE {database_name}"

        return self.__snowflake_connector.execute(statement, n=1, silent=silent)

    def get_current(
        self,
    ) -> str:
        """
        Returns the name of the database in use by the current session
        :return result dictionary (see: `SnowflakeConnector.execute()`)
        """
        statement = "SELECT CURRENT_DATABASE()"

        return self.__snowflake_connector.execute(statement, n=1)["results"][0][0]

    def create(self, database_name: str, or_replace: bool = False, silent: bool = False) -> Optional[Dict]:
        """
        Executes command to create a Snowflake database with a given name
        :param database_name: database name to create
        :param or_replace: replace database if exists
        :param silent: whether to run in silent mode (see `SnowflakeConnector.execute()`)
        :return result dictionary (see: `SnowflakeConnector.execute()`)
        """
        statement = "CREATE" f"{' OR REPLACE' if or_replace else ''}" f" DATABASE {database_name}"

        return self.__snowflake_connector.execute(statement, n=1, silent=silent)

    def drop(self, database_name: str, if_exists: bool = False, silent: bool = False) -> Optional[Dict]:
        """
        Executes command to drop a Snowflake database with a given name
        :param database_name: database name to drop
        :param if_exists: adds `IF EXISTS` statement to a command
        :param silent: whether to run in silent mode (see `SnowflakeConnector.execute()`)
        :return result dictionary (see: `SnowflakeConnector.execute()`)
        """
        statement = "DROP DATABASE" f"{' IF EXISTS' if if_exists else ''}" f" {database_name}"

        return self.__snowflake_connector.execute(statement, n=1, silent=silent)
