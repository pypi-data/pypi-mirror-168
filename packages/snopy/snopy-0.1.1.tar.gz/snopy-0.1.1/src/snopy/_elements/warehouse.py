from typing import Dict, List, Optional


class Warehouse:
    def __init__(self, snowflake_connector):
        self.__snowflake_connector = snowflake_connector

    def use(self, warehouse_name: str, silent: bool = False) -> Optional[Dict]:
        """
        Sets particular warehouse for a session
        :param warehouse_name: name of the warehouse to use
        :param silent: whether to run in silent mode (see `SnowflakeConnector.execute()`)
        :return result dictionary (see: `SnowflakeConnector.execute()`)
        """
        statement = "USE" f" WAREHOUSE {warehouse_name}"

        return self.__snowflake_connector.execute(statement, n=1, silent=silent)

    def get_current(
        self,
    ) -> str:
        """
        Returns the name of the warehouse in use by the current session
        :return result dictionary (see: `SnowflakeConnector.execute()`)
        """
        statement = "SELECT CURRENT_WAREHOUSE()"

        return self.__snowflake_connector.execute(statement, n=1)["results"][0][0]

    def create(
        self,
        warehouse_name: str,
        or_replace: bool = False,
        if_not_exists: bool = False,
        warehouse_size: str = "XSMALL",
        max_cluster_count: int = 1,
        min_cluster_count: int = 1,
        scaling_policy: str = "standard",
        auto_suspend: int = 600,
        auto_resume: bool = True,
        initially_suspended: bool = False,
        silent: bool = False,
        **kwargs,
    ) -> Optional[Dict]:
        """
        Creates a Snowflake virtual warehouse (compute layer) based on given parameters
        :param warehouse_name: database name to create
        :param or_replace: replaces warehosue if exists
        :param if_not_exists: only create the warehouse if another warehouse with the same name does not already exist
        :param warehouse_size: size of the virtual warehouse, passed in T-shirt sizing manner
        :param max_cluster_count: maximum number of clusters in multi-cluster warehouse deployment
        :param min_cluster_count: minimum number of clusters in multi-cluster warehouse deployment
        :param scaling_policy: policy for automatic starting and shutting down clusters in a multi-cluster deployment
        :param auto_suspend: number of seconds of inactivity after which warehosue is suspended automatically
        :param auto_resume: whether to automatically resume a warehouse when a SQL statement is submitted
        :param initially_suspended: whether the warehouse is created initially in the `Suspended` state
        :param silent: whether to run in silent mode (see `SnowflakeConnector.execute()`)
        :param kwargs: additional arguments to be passed to the statement,
            so far the validation is on the Snowflake engine side
        :return result dictionary (see: `SnowflakeConnector.execute()`)
        """
        statement = (
            "CREATE"
            f"{' OR REPLACE' if or_replace else ''}"
            " WAREHOUSE"
            f"{' IF NOT EXISTS' if if_not_exists else ''}"
            f" {warehouse_name} WITH"
            f" WAREHOUSE_SIZE = {warehouse_size}"
            f" MAX_CLUSTER_COUNT = {max_cluster_count}"
            f" MIN_CLUSTER_COUNT = {min_cluster_count}"
            f" SCALING_POLICY = {scaling_policy}"
            f" AUTO_SUSPEND = {auto_suspend}"
            f" AUTO_RESUME = {'TRUE' if auto_resume else 'FALSE'}"
            f" INITIALLY_SUSPENDED = {'TRUE' if initially_suspended else 'FALSE'}"
        )

        # looping through kwargs for extra arguments passed in statement
        # while executing final command, especially cloud-provider-specific parameters,
        # Snowflake will do the validation
        for key, value in kwargs.items():
            statement += f" {key} = {value}"

        return self.__snowflake_connector.execute(statement, n=1, silent=silent)
