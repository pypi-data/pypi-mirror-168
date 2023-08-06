from typing import Dict, List, Optional


class Stage:
    def __init__(self, snowflake_connector):
        self.__snowflake_connector = snowflake_connector

    def create(
        self,
        stage_name: str,
        or_replace: bool = False,
        is_temporary: bool = False,
        if_not_exists: bool = False,
        file_format_name: str = "",
        silent: bool = False,
        **kwargs,
    ) -> Optional[Dict]:
        """
        Executes command to create a Snowflake stage with a given name
        :param stage_name: stage name to create
        :param or_replace: replace file format if exists
        :param is_temporary: create a temporary stage
        :param if_not_exists: create object if it doesn't exist so far
        :param file_format_name: file format name to use while creating a stage
        :param silent: whether to run in silent mode (see `SnowflakeConnector.execute()`)
        :param kwargs: additional arguments to be passed to the statement,
            so far the validation is on the Snowflake engine side
        :return result dictionary (see: `SnowflakeConnector.execute()`)
        """
        statement = (
            "CREATE"
            f"{' OR REPLACE' if or_replace else ''}"
            f"{' TEMPORARY' if is_temporary else ''}"
            f" STAGE"
            f"{' IF NOT EXISTS' if if_not_exists else ''}"
            f" {stage_name}"
            f"{f' FILE_FORMAT = {file_format_name}' if file_format_name != '' else ''}"
        )

        # looping through kwargs for extra arguments passed in statement
        # while executing final command, Snowflake will do the validation
        for key, value in kwargs.items():
            statement += f" {key} = {value}"

        return self.__snowflake_connector.execute(statement, n=1, silent=silent)

    def drop(self, stage_name: str, if_exists: bool = False, silent: bool = False) -> Optional[Dict]:
        """
        Executes command to drop a Snowflake stage with a given name
        :param stage_name: stage name to drop
        :param if_exists: adds `IF EXISTS` statement to a command
        :param silent: whether to run in silent mode (see `SnowflakeConnector.execute()`)
        :return result dictionary (see: `SnowflakeConnector.execute()`)
        """
        statement = "DROP STAGE" f"{' IF EXISTS' if if_exists else ''}" f" {stage_name}"

        return self.__snowflake_connector.execute(statement, n=1, silent=silent)

    def put(
        self,
        filepath: str,
        internal_stage_name: str,
        parallel: int = 4,
        auto_compress: bool = True,
        source_compression: str = "AUTO_DETECT",
        overwrite: bool = False,
        silent: bool = False,
    ) -> Optional[Dict]:
        """
        Executes command to put data to Snowflake internal stage from a local machine
        :param filepath: local path to a file
        :param internal_stage_name: stage name where to put file a file
            Caution: when having problems with this param, please check whether you specify the proper
            internal stage name, including special signs: @, %, and ~
        :param parallel: number of threads to use for uploading files
        :param auto_compress: whether Snowflake uses gzip to compress files during upload
        :param source_compression: method of compression used on already-compressed files that are being staged
        :param overwrite: whether Snowflake overwrites an existing file with the same name during upload
        :param silent: whether to run in silent mode (see `SnowflakeConnector.execute()`)
        :return result dictionary (see: `SnowflakeConnector.execute()`)
        """
        statement = (
            "PUT"
            f" '{filepath}'"
            f" {internal_stage_name}"
            f" PARALLEL = {parallel}"
            f" AUTO_COMPRESS = {'TRUE' if auto_compress else 'FALSE'}"
            f" SOURCE_COMPRESSION = {source_compression}"
            f" OVERWRITE = {'TRUE' if overwrite else 'FALSE'}"
        )

        return self.__snowflake_connector.execute(statement, n=1, silent=silent)

    def list(self, stage_name: str, regex_pattern: str = "", silent: bool = False) -> Optional[Dict]:
        """
        Lists files that are inside in a particular stage
        :param stage_name: the location where the data files are staged
        :param regex_pattern: a regular expression pattern for filtering files from the output
        :param silent: whether to run in silent mode (see `SnowflakeConnector.execute()`)
        :return result dictionary (see: `SnowflakeConnector.execute()`)
        """
        statement = "LIST" f" {stage_name}" f"{f' PATTERN = {regex_pattern}' if regex_pattern != '' else ''}"

        return self.__snowflake_connector.execute(statement, n=1, silent=silent)
