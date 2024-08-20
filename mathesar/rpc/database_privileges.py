from typing import TypedDict

from modernrpc.core import rpc_method, REQUEST_KEY
from modernrpc.auth.basic import http_basic_auth_login_required

from db.roles.operations.select import list_db_priv, get_curr_role_db_priv
from mathesar.rpc.utils import connect
from mathesar.models.base import Database
from mathesar.rpc.exceptions.handlers import handle_rpc_exceptions


class DBPrivileges(TypedDict):
    """
    Information about database privileges.

    Attributes:
        role_oid: The `oid` of the role on the database server.
        direct: A list of database privileges for the afforementioned role_oid.
    """
    role_oid: int
    direct: list[str]

    @classmethod
    def from_dict(cls, d):
        return cls(
            role_oid=d["role_oid"],
            direct=d["direct"]
        )


class CurrentDBPrivileges(TypedDict):
    """
    Information about database privileges for current user.

    Attributes:
        owner_oid: The `oid` of the owner of the database.
        current_role_db_priv: A list of database privileges for the current user.
    """
    owner_oid: int
    current_role_db_priv: list[str]

    @classmethod
    def from_dict(cls, d):
        return cls(
            owner_oid=d["owner_oid"],
            current_role_db_priv=d["current_role_db_priv"]
        )


@rpc_method(name="database_privileges.list_direct")
@http_basic_auth_login_required
@handle_rpc_exceptions
def list_direct(*, database_id: int, **kwargs) -> list[DBPrivileges]:
    """
    List database privileges for non-inherited roles.

    Args:
        database_id: The Django id of the database.

    Returns:
        A list of database privileges.
    """
    user = kwargs.get(REQUEST_KEY).user
    with connect(database_id, user) as conn:
        db_name = Database.objects.get(id=database_id).name
        raw_db_priv = list_db_priv(db_name, conn)
    return [DBPrivileges.from_dict(i) for i in raw_db_priv]


# TODO: Think of something concise for the endpoint name.
@rpc_method(name="database_privileges.get_owner_oid_and_curr_role_db_priv")
@http_basic_auth_login_required
@handle_rpc_exceptions
def get_owner_oid_and_curr_role_db_priv(*, database_id: int, **kwargs) -> CurrentDBPrivileges:
    """
    Get database privileges for the current user.

    Args:
        database_id: The Django id of the database.

    Returns:
        A dict describing current user's database privilege.
    """
    user = kwargs.get(REQUEST_KEY).user
    with connect(database_id, user) as conn:
        db_name = Database.objects.get(id=database_id).name
        curr_role_db_priv = get_curr_role_db_priv(db_name, conn)
    return CurrentDBPrivileges.from_dict(curr_role_db_priv)