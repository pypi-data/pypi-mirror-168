from typing import Dict, List, Optional


class StorageIntegration:
    def __init__(self, snowflake_connector):
        self.__snowflake_connector = snowflake_connector

    def create(
        self,
        storage_integration_name: str,
        storage_provider: str,
        storage_allowed_locations: List[str],
        or_replace: bool = False,
        if_not_exists: bool = False,
        enabled: bool = True,
        silent: bool = False,
        **kwargs,
    ) -> Optional[Dict]:
        """
        Executes command to create a Snowflake stage with a given name
        :param storage_integration_name: storage integration name to create
        :param storage_provider: cloud provider to create stage and fetch data from
        :param storage_allowed_locations: explicitly limits external stages
            that use the integration to reference one or more storage locations
        :param or_replace: replace file format if exists
        :param if_not_exists: create object if it doesn't exist so far
        :param enabled: specifies whether this storage integration is available for usage in stages
        :param silent: whether to run in silent mode (see `SnowflakeConnector.execute()`)
        :param kwargs: additional arguments to be passed to the statement,
            so far the validation is on the Snowflake engine side
        :return result dictionary (see: `SnowflakeConnector.execute()`)
        """
        storage_allowed_loccations_string = ",".join([f"'{file}'" for file in storage_allowed_locations])

        statement = (
            "CREATE"
            f"{' OR REPLACE' if or_replace else ''}"
            f" STORAGE INTEGRATION{' IF NOT EXISTS' if if_not_exists else ''} {storage_integration_name}"
            f" TYPE = EXTERNAL_STAGE"
            f" ENABLED = {'TRUE' if enabled else 'FALSE'}"
            f" STORAGE_PROVIDER = {storage_provider}"
            f" STORAGE_ALLOWED_LOCATIONS = ({storage_allowed_loccations_string})"
        )

        # looping through kwargs for extra arguments passed in statement
        # while executing final command, especially cloud-provider-specific parameters,
        # Snowflake will do the validation
        for key, value in kwargs.items():
            statement += f" {key} = {value}"

        return self.__snowflake_connector.execute(statement, n=1, silent=silent)

    def drop(
        self,
        storage_integration_name: str,
        if_exists: bool = False,
        silent: bool = False,
    ) -> Optional[Dict]:
        """
        Executes command to drop a Snowflake storage integration with a given name
        :param storage_integration_name: storage integration name to drop
        :param if_exists: adds `IF EXISTS` statement to a command
        :param silent: whether to run in silent mode (see `SnowflakeConnector.execute()`)
        :return result dictionary (see: `SnowflakeConnector.execute()`)
        """
        statement = "DROP STORAGE INTEGRATION" f"{' IF EXISTS' if if_exists else ''}" f" {storage_integration_name}"

        return self.__snowflake_connector.execute(statement, n=1, silent=silent)
