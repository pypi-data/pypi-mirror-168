import os
from typing import Optional, Tuple

from airflow.models.connection import Connection
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.context import Context
from airflow.utils.decorators import apply_defaults
from sqlalchemy import create_engine

if TYPE_CHECKING:
    from sqlalchemy.engine.base import Engine


def get_azure_token_with_msi() -> str:
    """Retreive Azure token for access referentie database.

    By using the Managed Idenity (MI) of Airflow instance on Azure AKS
    an access token is retrieved. The MI has to be a member of the Azure AD
    group that is used as a database user to login into the referentie database.

    returns:
        Access token for database user based on the Managed Idenity (MI) of Airflow instance.
    """
    # database scope definition for getting Azure access token based on MI of Airflow.
    AZURE_RDBMS_RESOURCE_ID: Final = 'https://ossrdbms-aad.database.windows.net/.default'

    credential = DefaultAzureCredential()
    scope = AZURE_RDBMS_RESOURCE_ID
    access_token = credential.get_token(scope).token

    return str(access_token)


def generate_dbuser_azure(dataset_name: str) -> str:
    """Generating database users for access referentie database on Azure.

    Database users names have the convention:
    `EM4W-DATA-dataset-[ot|ap]-[name-of-dataset-in-snake-case]`

    TODO: There is extra complexity where a seperate db user is present
    for datasets that contain tables that fall in more then one dataset layer.
    Like: https://schemas.data.amsterdam.nl/datasets/wegenbestand/zoneZwaarVerkeer/breedOpgezetteWegen/
    However, there is one DAG that processes the data. Since there is one source and one topic
    (wegenbestand). Because each dataset correspondents to one user, there will be 2 separate
    users: wegenbestand and zoneZwaarVerkeer. This is needs to be figured out in more dept how to
    go about in the DAG.

    Args:
        dataset_name: Name of the dataset as known in the Amsterdam schema.
            The dataset name refers to an Azure AD group where the Airflow Managed Idenity (MI)
            is member of. Only applicable to Azure connections.

    returns:
        database user name for accessing Azure referentie database

	"""
    # depending on the Azure environment, the db user name will be containing `ot` or `ap`.
    otap_env = os.environ.get('AZURE_OTAP_ENVIRONMENT')

    if otap_env is None:
        raise ValueError("AZURE_OTAP_ENVIRONMENT is not set. Cannot determine db user environment context. please check your values.")
    elif 'ont' in otap_env or 'tst' in otap_env:
        db_user = f"EM4W-DATA-dataset-ot-{to_snake_case(dataset_name)}-rw"

    elif 'acc' in otap_env or 'prd' in otap_env:
        db_user = f"EM4W-DATA-dataset-ap-{to_snake_case(dataset_name)}-rw"

    return db_user


def define_dataset_name_for_azure_dbuser(context: Optional[Context] = None, dataset_name: Optional[str] = None) -> str:
    """Defining the dataset name as part of the user Azure referentie database.

    Each dataset will have its own database user on Azure referentie
    database. The dataset name will be part of the user name. Like so:
    `EM4W-DATA-dataset-[ot|ap]-[name-of-dataset-in-snake-case]`

    If the dataset name is ommitted then the DAG id will be
    used. Assuming that the DAG is equals the dataset name.

    args:
        dataset_name: Name of the dataset as known in the Amsterdam schema.
            Since the DAG name can be different from the dataset name, the latter
            can be explicity given. Only applicable for Azure referentie db connection.
            Defaults to None. If None, it will use the execution context to get the
            DAG id as surrogate. Assuming that the DAG id equals the dataset name
            as defined in Amsterdam schema.
        context: The context of run-time process that calls this function.
            Can be used to derive the DAG id as surrogate for database user
            if the dataset_name parameter is ommited.

    returns:
        Name of database user to login on Azure referentie database.
    """
    if dataset_name is None:
        if context is not None:
            dataset_name = context['task_id'].dag_id
        else:
            # both dataset_name and context are None
            raise AirflowException("""cannot define dataset name as part of Azure db user,
                both dataset_name and context are None.""")
    return dataset_name


class PostgresOnAzureHook(PostgresHook):
    """Postgres connection hook for Azure."""

    @apply_defaults  # type: ignore[misc]
    def __init__(
        self, context: Context, dataset_name: Optional[str] = None, *args: Any, **kwargs: Any
    ) -> None:
        """Initialize.

        Args:
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

    def execute(self, context: Context) -> None:
        """Runs after __init__."""
        # Due to circular import moved into method.
        # Reason: The PostgresOnAzureHook itself is also imported from
        # within `common.db`.        #
        from common.db import define_dataset_name_for_azure_dbuser

        # If Azure.
        # To cope with a different logic for defining the Azure referentie db user.
        # If CloudVPS is not used anymore, then this extra route can be removed.
        if os.environ.get("AZURE_TENANT_ID") is not None:
            # define the dataset name as part of the db user.
            self.dataset_name = define_dataset_name_for_azure_dbuser(
                dataset_name=self.dataset_name, context=self.context
            )

    def get_iam_token(self, conn: Connection) -> tuple[str, str, int]:
        """Override PostgresHook get_iam_token with Azure logic.

        NOTE:
        This method only gets executed if in the connection string the parameter `iam=true`
        is added. Applicable for Azure connections.

        This class uses `DefaultAzureCredential` which will pick up the managed identity
        using the `AZURE_TENANT_ID` and `AZURE_CLIENT_ID` environment variables.
        Then set the connection like this:
        "postgresql://EM4W-DATA-dataset-ot-covid_19-rw@<hostname>:<token>@\
            <hostname>.postgres.database.azure.com:5432/<db_name>?cursor=dictcursor&iam=true"

        The AAD group needs to be registered in the database as an AAD related user.
        See https://docs.microsoft.com/en-us/azure/postgresql/single-server/\
            how-to-configure-sign-in-azure-ad-authentication#authenticate-with-azure-ad-as-a-group-member
        for reference

        Args:
            conn: Name of database connection as defined as airflow_conn_XXX.

        Returns:
            database user, password (token) and port number.
        """
        # Due to circular import moved into method.
        # Reason: The PostgresOnAzureHook itself is also imported from
        # within `common.db`.
        from common.db import generate_dbuser_azure, get_azure_token_with_msi

        username = generate_dbuser_azure(self.dataset_name)
        login = conn.login.replace(
            "AAD-GROUP-NAME-REPLACED-BY-AIRFLOW", username
        )  # must be <group_name>@<server_name>
        password = get_azure_token_with_msi()

        if conn.port is None:
            port = 5432
        else:
            port = conn.port

        return login, password, port


    def get_sqlalchemy_engine(self, split_dictcursor:bool = False, engine_kwargs: Any =None) -> 'Engine':
        """Override of `get_sqlalchemy_engine` method in DbApiHook.

        When doing an execute() on get_sqlalchemy_engine() the
        psycopg2.extensions.parse_dsn() will raise and invalid dsn
        option `cursor`. Therefor the cursor URL parameter is removed.
        This is probably caused since the upgrade of SQLalchemy to 1.4.27.

        :param engine_kwargs: Kwargs used in :func:`~sqlalchemy.create_engine`.
        :return: An sqlalchemy_engine object; the created engine.
        """
        if split_dictcursor:
            get_uri = self.get_uri().split('?cursor=dictcursor')[0]
        else:
            get_uri = self.get_uri()

        if engine_kwargs is None:
            engine_kwargs = {}
        return create_engine(get_uri, **engine_kwargs)
