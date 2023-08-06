from typing import Dict, List, Optional


class Role:
    def __init__(self, snowflake_connector):
        self.__snowflake_connector = snowflake_connector

    def use(self, role_name: str, silent: bool = False) -> Optional[Dict]:
        """
        Sets particular role for a session
        :param role_name: name of the role to use
        :param silent: whether to run in silent mode (see `SnowflakeConnector.execute()`)
        :return result dictionary (see: `SnowflakeConnector.execute()`)
        """
        statement = "USE" f" ROLE {role_name}"

        return self.__snowflake_connector.execute(statement, n=1, silent=silent)

    def get_current(
        self,
    ) -> str:
        """
        Returns the name of the role in use by the current session
        :return result dictionary (see: `SnowflakeConnector.execute()`)
        """
        statement = "SELECT CURRENT_ROLE()"

        return self.__snowflake_connector.execute(statement, n=1)["results"][0][0]
