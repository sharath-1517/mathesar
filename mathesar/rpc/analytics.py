"""
Classes and functions exposed to the RPC endpoint for managing analytics.
"""
from typing import TypedDict, Optional
from mathesar.rpc.decorators import mathesar_rpc_method
from mathesar.analytics import (
    initialize_analytics,
    disable_analytics,
    prepare_analytics_report,
)


class AnalyticsReport(TypedDict):
    """
    A report with some statistics about the data accessible by Mathesar.

    Attributes:
        installation_id: A unique ID for this Mathesar installation.
        mathesar_version: The version of Mathesar.
        user_count: The number of configured users in Mathesar.
        active_user_count: The number of users who have recently logged in.
        configured_role_count: The number of DB roles configured.
        connected_database_count: The number of databases configured.
        connected_database_schema_count: The number of all schemas in
            all connected databases.
        connected_database_table_count: The total number of tables in
            all conncted databasees.
        connected_database_record_count: The total number of records in
            all connected databasees (approximated)
        exploration_count: The number of explorations.
    """
    installation_id: Optional[str]
    mathesar_version: str
    user_count: int
    active_user_count: int
    configured_role_count: int
    connected_database_count: int
    connected_database_schema_count: int
    connected_database_table_count: int
    connected_database_record_count: int
    exploration_count: int

    @classmethod
    def from_dict(cls, d):
        if d["installation_id"] is not None:
            d["installation_id"] = str(d["installation_id"].value)
        return cls(d)


@mathesar_rpc_method(name="analytics.initialize")
def initialize():
    """
    Initialize analytics collection and reporting in Mathesar

    If initialized, analytics are gathered to a local model once per day,
    and uploaded.
    """
    initialize_analytics()


@mathesar_rpc_method(name="analytics.disable")
def disable():
    """
    Disable analytics collection and reporting in Mathesar

    Disabling analytics amounts to (for now) simply deleting the
    Installation ID, ensuring that it's impossible to save analytics
    reports. Any reports currently saved are removed when the
    Installation ID is deleted.
    """
    disable_analytics()


@mathesar_rpc_method(name="analytics.view_report")
def view_report() -> AnalyticsReport:
    """
    View an example analytics report, prepared with the same function
    that creates real reports that would be saved and uploaded.

    Returns:
        An analytics report.
    """
    report = prepare_analytics_report()
    return AnalyticsReport.from_dict(report)