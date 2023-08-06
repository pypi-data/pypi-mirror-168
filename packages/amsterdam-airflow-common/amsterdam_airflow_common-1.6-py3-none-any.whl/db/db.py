from typing import Dict
import cx_Oracle
import dsnparse
from airflow import AirflowException
from airflow.hooks.base import BaseHook
from airflow.utils.context import Context
from airflow.utils.decorators import apply_defaults
from airflow.providers.oracle.hooks.oracle import OracleHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from geoalchemy2 import WKTElement
from shapely import wkt
from shapely.geometry.multipolygon import MultiPolygon
from shapely.geometry.polygon import Polygon
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError


def pg_params(conn_id: str = "postgres_default") -> str:
    """Add "stop on error" argument to connection string.

    Args:
        conn_id: database connection that is provided with default parameters
    returns:
        connection string with default params
    """
    connection_uri = BaseHook.get_connection(conn_id).get_uri().split("?")[0]
    return f"{connection_uri} -X --set ON_ERROR_STOP=1"


class DatabaseEngine:
    """Construct the elements of the SQLAlchemy database engine."""

    def __init__(self, postgres_conn_id: str = "postgres_default"):
        """Initialize DatabaseEngine."""
        self.connection = PostgresHook().get_connection(postgres_conn_id)
        self.user = self.connection.login
        self.password = self.connection.password
        self.host = self.connection.host
        self.port = self.connection.port
        self.db = self.connection.schema


def get_postgreshook_instance(postgres_conn_id: str = "postgres_default") -> PostgresHook:
    """Return a postgreshook instance.

    So it can be used to get connection i.e.
    """
    connection = PostgresHook(postgres_conn_id=postgres_conn_id)
    return connection


def get_engine(postgres_conn_id: str = "postgres_default") -> Engine:
    """Construct the SQLAlchemy database engine."""
    connection = PostgresHook().get_connection(postgres_conn_id)
    user = connection.login
    password = connection.password
    host = connection.host
    port = connection.port
    db = connection.schema

    try:
        return create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")
    except SQLAlchemyError as e:
        raise AirflowException(str(e)) from e


def get_ora_engine(oracle_conn_id: str = "oracle_default") -> Engine:
    """Get the oracle connection parameters.

    Some KPN's Oracle databases are provided in a container that cannot
        be accessed by a SID.
    A service_name parameter must be provided in the connection string to
        make the connection to the source DB.
    The OracleHook provides a method get_conn() that can be used to setup
        the connection by service_name.
    More info:
    https://airflow.apache.org/docs/apache-airflow-providers-oracle/stable/_modules/airflow/providers/oracle/hooks/oracle.html#OracleHook.get_conn
    """  # noqa: E501
    conn_instance = OracleHook(oracle_conn_id=oracle_conn_id)
    return conn_instance


def fetch_pg_env_vars(postgres_conn_id: str = "postgres_default") -> Dict[str, str]:
    """Get the Postgres Default DSN connection info as a dict."""
    # Need to get rid of trailing '&'
    # moved from to here due to circular import error
    from . import env

    stripped_env = env("AIRFLOW_CONN_POSTGRES_DEFAULT")[:-1]
    pg_conn_info = dsnparse.parse(stripped_env)
    return {
        "PGHOST": pg_conn_info.host,
        "PGPORT": str(pg_conn_info.port),
        "PGDATABASE": pg_conn_info.paths[0],
        "PGUSER": pg_conn_info.username,
        "PGPASSWORD": pg_conn_info.password,
    }


def wkt_loads_wrapped(data: str, source_srid: int) -> WKTElement:
    """Loading WKT (well known text) geometry definition.

    This function translates a single geometry to multi
    and processes an Oracle LOB datatype (if present).

    Args:
        data: Geometry data from source.
        source_srid: SRID of the source geometry data.

    Returns:
        A WKTElement object of the geometry data.
    """
    if isinstance(data, cx_Oracle.LOB):
        data = data.read()

    if data is not None:
        p = wkt.loads(data)
        if isinstance(p, Polygon):
            p = MultiPolygon([p])
        elif isinstance(p, MultiPolygon):
            pass
        else:
            p = p
        p = WKTElement(p.wkt, srid=source_srid)
        return p


class PostgresOnAzureHook(PostgresHook):
    """Postgres connection hook for Azure."""

    @apply_defaults  # type: ignore[misc]
    def __init__(self, context:Context, dataset_name:Optional[str] = None, *args, **kwargs) -> None:
        """Initialize.

        args:
            dataset_name: Name of the dataset as known in the Amsterdam schema.
                Since the DAG name can be different from the dataset name, the latter
                can be explicity given. Only applicable for Azure referentie db connection.
                Defaults to None. If None, it will use the execution context to get the
                DAG id as surrogate. Assuming that the DAG id equals the dataset name
                as defined in Amsterdam schema.
            context: The execution context. It is used when no dataset_name is given.
                Based on the DAG id - extracted from the execution context - the dataset_name
                is derived. Assuming that the DAG id equals the dataset name as defined in
                Amsterdam schema.
        """
        self.dataset_name = dataset_name
        self.context = context
        super().__init__(*args, **kwargs)

    def execute(self, context: Context):
        """Runs after __init__."""
        # If Azure.
        # To cope with a different logic for defining the Azure referentie db user.
        # If CloudVPS is not used anymore, then this extra route can be removed.
        if os.environ.get("AZURE_TENANT_ID") is not None:
            # define the dataset name as part of the db user.
            self.dataset_name = define_dataset_name_for_azure_dbuser(dataset_name=self.dataset_name, context=self.context)

    def get_iam_token(self, conn: Connection) -> Tuple[str, str, int]:
        """Override PostgresHook get_iam_token with Azure logic.

        This method only gets executed if in the connection string the parameter `iam=true`
        is added. Applicable for Azure connections.

        This class uses `DefaultAzureCredential` which will pick up the managed identity
        using the `AZURE_TENANT_ID` and `AZURE_CLIENT_ID` environment variables.
        Then set the connection like this:
        "postgresql://EM4W-DATA-dataset-ot-covid_19-rw@<hostname>:<token>@\
            <hostname>.postgres.database.azure.com:5432/<db_name>?cursor=dictcursor&iam=true"

        NOTE:
        The AAD group needs to be registered in the database as an AAD related user.
        See https://docs.microsoft.com/en-us/azure/postgresql/single-server/\
            how-to-configure-sign-in-azure-ad-authentication#authenticate-with-azure-ad-as-a-group-member
        for reference

        args:
            conn: Name of database connection as defined as airflow_conn_XXX.

        returns:
            database user, password (token) and port number.
        """
        username = generate_dbuser_azure(self.dataset_name)
        login = conn.login.replace('AAD-GROUP-NAME-REPLACED-BY-AIRFLOW', username)  # must be <group_name>@<server_name>
        password = get_azure_token_with_msi()

        if conn.port is None:
            port = 5432
        else:
            port = conn.port

        return login, password, port
