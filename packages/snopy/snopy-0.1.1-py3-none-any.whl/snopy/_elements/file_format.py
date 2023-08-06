from typing import Dict, List, Optional


class FileFormat:
    def __init__(self, snowflake_connector):
        self.__snowflake_connector = snowflake_connector
        self.__AVAILABLE_FORMAT_TYPES = ["CSV", "JSON", "AVRO", "ORC", "PARQUET", "XML"]

    def create(
        self,
        file_format_name: str,
        file_format_type: str,
        or_replace: bool = False,
        if_not_exists: bool = False,
        silent: bool = False,
        **kwargs,
    ) -> Optional[Dict]:
        """
        Executes command to create a Snowflake file format with a given name
        :param file_format_name: file format name to create
        :param file_format_type: type of the file format to be created
        :param or_replace: replace file format if exists
        :param if_not_exists: create object if it doesn't exist so far
        :param silent: whether to run in silent mode (see `SnowflakeConnector.execute()`)
        :param kwargs: additional arguments to be passed to the statement
            so far validation is on the Snowflake engine side
        :return result dictionary (see: `SnowflakeConnector.execute()`)
        """
        file_format_type = file_format_type.upper().strip()
        if file_format_type not in self.__AVAILABLE_FORMAT_TYPES:
            raise ValueError(f"File Format type `{file_format_type}` not available for now")

        statement = (
            "CREATE"
            f"{' OR REPLACE' if or_replace else ''}"
            f" FILE FORMAT{' IF NOT EXISTS' if if_not_exists else ''} {file_format_name}"
            f" TYPE = {file_format_type}"
        )

        # looping through kwargs for extra arguments passed in statement
        # while executing final command, Snowflake will do the validation
        for key, value in kwargs.items():
            statement += f" {key} = {value}"

        return self.__snowflake_connector.execute(statement, n=1, silent=silent)

    def drop(self, file_format_name: str, if_exists: bool = False, silent: bool = False) -> Optional[Dict]:
        """
        Executes command to drop a Snowflake file format with a given name
        :param file_format_name: file format name to drop
        :param if_exists: adds `IF EXISTS` statement to a command
        :param silent: whether to run in silent mode (see `SnowflakeConnector.execute()`)
        :return result dictionary (see: `SnowflakeConnector.execute()`)
        """
        statement = "DROP FILE FORMAT" f"{' IF EXISTS' if if_exists else ''}" f" {file_format_name}"

        return self.__snowflake_connector.execute(statement, n=1, silent=silent)
