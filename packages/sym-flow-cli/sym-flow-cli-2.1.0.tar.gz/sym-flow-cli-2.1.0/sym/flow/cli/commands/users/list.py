from typing import List

import click
from tabulate import tabulate

from sym.flow.cli.helpers.api import SymAPI
from sym.flow.cli.helpers.global_options import GlobalOptions
from sym.flow.cli.helpers.utils import human_friendly, utc_to_local


@click.command(name="list", short_help="List all Users")
@click.make_pass_decorator(GlobalOptions, ensure=True)
def users_list(options: GlobalOptions) -> None:
    """Lists all Users in your organization.

    Note: To see a list of all User identities, use:

        `symflow users list-identities`
    """
    table_data = get_user_data(options.sym_api)
    click.echo(tabulate(table_data, headers="firstrow"))


def get_user_data(api: SymAPI) -> List[List[str]]:
    table_data = [["Email", "Role", "Created At"]]
    for user in api.get_users():
        created_at = human_friendly(utc_to_local(user.created_at))  # type: ignore
        table_data.append([user.sym_email, "admin" if user.is_admin else "", created_at])

    return table_data
