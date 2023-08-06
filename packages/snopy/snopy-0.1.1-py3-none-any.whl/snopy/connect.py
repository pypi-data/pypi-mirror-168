from snopy._elements.snowflake_connector import SnowflakeConnector


def snopy_connect(
    account: str,
    username: str,
    password: str,
    warehouse: str = "",
    database: str = "",
    schema: str = "",
    role: str = "",
) -> SnowflakeConnector:
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
    :return Snowflake Connector object
    """
    return SnowflakeConnector(
        account=account,
        username=username,
        password=password,
        warehouse=warehouse,
        database=database,
        schema=schema,
        role=role,
    )
