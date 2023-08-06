
# This is a command file for our CLI. Please keep it clean.
#
# - If it makes sense and only when strictly necessary, you can create utility functions in this file.
# - But please, **do not** interleave utility functions and command definitions.

from copy import deepcopy
import click
from click import Context

import humanfriendly
from tinybird.client import TinyB
from tinybird.feedback_manager import FeedbackManager
from tinybird.tb_cli_modules.common import ask_for_user_token, coro, get_config_and_hosts, get_current_workspace
from tinybird.tb_cli_modules.workspace import workspace


@workspace.group()
@click.pass_context
def members(ctx):
    '''Workspace members management commands'''


@members.command(name='add', short_help="Adds members to the current Workspace")
@click.argument('members_emails')
@click.option('--user_token', is_flag=False, default=None, help="Do not ask for your user token")
@click.pass_context
@coro
async def add_members_to_workspace(ctx: Context, members_emails: str, user_token: str):
    """Adds members to the current Workspace"""

    client: TinyB = ctx.ensure_object(dict)['client']
    config, host, ui_host = await get_config_and_hosts(ctx)

    workspace = await get_current_workspace(client, config)
    if workspace is None:
        raise click.ClickException(FeedbackManager.error_unknown_resource(resource=config['d']))  # type: ignore

    requested_users = members_emails.split(',')
    existing_users = [u['email'] for u in workspace['members']]
    users_to_add = [u for u in requested_users if u not in existing_users]

    if len(users_to_add) == 0:
        msg = FeedbackManager.info_user_already_exists(user=requested_users[0], workspace_name=workspace['name']) if len(requested_users) == 1 else FeedbackManager.info_users_already_exists(workspace_name=workspace['name'])
        click.echo(msg)
    else:
        if not user_token:
            user_token = ask_for_user_token(f"add users to {workspace['name']}", ui_host)

        user_client: TinyB = deepcopy(client)
        user_client.token = user_token
        await user_client.add_users_to_workspace(workspace, users_to_add)
        msg = FeedbackManager.success_workspace_user_added(user=users_to_add[0], workspace_name=workspace['name']) if len(users_to_add) == 1 else FeedbackManager.success_workspace_users_added(workspace_name=workspace['name'])
        click.echo(msg)


@members.command(name='ls', short_help="List members in the current Workspace")
@click.pass_context
@coro
async def list_members_in_workspace(ctx: Context):
    """List members in the current Workspace"""

    client: TinyB = ctx.ensure_object(dict)['client']
    config, host, ui_host = await get_config_and_hosts(ctx)

    workspace = await get_current_workspace(client, config)
    if workspace is None:
        raise click.ClickException(FeedbackManager.error_unknown_resource(resource=config['d']))  # type: ignore

    existing_users = [[u['email']] for u in workspace['members']]
    print(humanfriendly.tables.format_smart_table(existing_users, column_names=['email']))


@members.command(name='rm', short_help="Removes members from the current Workspace")
@click.argument('members_emails')
@click.option('--user_token', is_flag=False, default=None, help="Do not ask for your user token")
@click.pass_context
@coro
async def remove_members_from_workspace(ctx: Context, members_emails: str, user_token: str):
    """Removes members from the current Workspace"""

    client: TinyB = ctx.ensure_object(dict)['client']
    config, host, ui_host = await get_config_and_hosts(ctx)

    workspace = await get_current_workspace(client, config)
    if workspace is None:
        raise click.ClickException(FeedbackManager.error_unknown_resource(resource=config['d']))  # type: ignore

    requested_users = members_emails.split(',')
    existing_users = [u['email'] for u in workspace['members']]
    users_to_remove = [u for u in requested_users if u in existing_users]

    if len(users_to_remove) == 0:
        msg = FeedbackManager.info_user_not_exists(user=requested_users[0], workspace_name=workspace['name']) if len(requested_users) == 1 else FeedbackManager.info_users_not_exists(workspace_name=workspace['name'])
        click.echo(msg)
    else:
        if not user_token:
            user_token = ask_for_user_token(f"remove users from {workspace['name']}", ui_host)

        user_client: TinyB = deepcopy(client)
        user_client.token = user_token
        await user_client.remove_users_from_workspace(workspace, users_to_remove)
        msg = FeedbackManager.success_workspace_user_removed(user=users_to_remove[0], workspace_name=workspace['name']) if len(users_to_remove) == 1 else FeedbackManager.success_workspace_users_removed(workspace_name=workspace['name'])
        click.echo(msg)
