from typing import Dict, List, Optional


class Schema:
    def __init__(self, snowflake_connector):
        self.__snowflake_connector = snowflake_connector

    def use(self, schema_name: str, silent: bool = False) -> Optional[Dict]:
        """
        Sets particular schema for a session
        :param schema_name: name of the schema to use
        :param silent: whether to run in silent mode (see `SnowflakeConnector.execute()`)
        :return result dictionary (see: `SnowflakeConnector.execute()`)
        """
        statement = "USE" f" SCHEMA {schema_name}"

        return self.__snowflake_connector.execute(statement, n=1, silent=silent)

    def get_current(
        self,
    ) -> str:
        """
        Returns the name of the schema in use by the current session
        :return result dictionary (see: `SnowflakeConnector.execute()`)
        """
        statement = "SELECT CURRENT_SCHEMA()"

        return self.__snowflake_connector.execute(statement, n=1)["results"][0][0]

    def create(self, schema_name: str, or_replace: bool = False, silent: bool = False) -> Optional[Dict]:
        """
        Executes command to create a Snowflake schema with a given name
        :param schema_name: schema name to create
        :param or_replace: replace schema if exists
        :param silent: whether to run in silent mode (see `SnowflakeConnector.execute()`)
        :return result dictionary (see: `SnowflakeConnector.execute()`)
        """
        statement = "CREATE" f"{' OR REPLACE' if or_replace else ''}" f" SCHEMA {schema_name}"

        return self.__snowflake_connector.execute(statement, n=1, silent=silent)

    def drop(self, schema_name: str, if_exists: bool = False, silent: bool = False) -> Optional[Dict]:
        """
        Executes command to drop a Snowflake schema with a given name
        :param schema_name: schema name to drop
        :param if_exists: adds `IF EXISTS` statement to a command
        :param silent: whether to run in silent mode (see `SnowflakeConnector.execute()`)
        :return result dictionary (see: `SnowflakeConnector.execute()`)
        """
        statement = "DROP SCHEMA" f"{' IF EXISTS' if if_exists else ''}" f" {schema_name}"

        return self.__snowflake_connector.execute(statement, n=1, silent=silent)
