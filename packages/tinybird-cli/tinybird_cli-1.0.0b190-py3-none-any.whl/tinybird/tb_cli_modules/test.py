
# This is a command file for our CLI. Please keep it clean.
#
# - If it makes sense and only when strictly necessary, you can create utility functions in this file.
# - But please, **do not** interleave utility functions and command definitions.

import glob
import click

from tinybird.tb_cli_modules.cli import cli
from tinybird.tb_cli_modules.common import coro, create_tb_client
from tinybird.tb_cli_modules.tinyunit.tinyunit import test_file_add_test, test_file_reload_test, test_file_remove_test, test_file_set_test_state, test_file_show_test, tinyUnitRunner


@cli.group()
@click.pass_context
def test(ctx):
    '''Test commands'''


@test.command(name="add", help="Adds a test to a file. Example usage: tb test add --file test/my_endpoint.json --sql select 1 as this_always_fail")
@click.option('--file', help='the destination test file. i.e tests/my_test.json', type=str, default='tests/default.json')
@click.option('--endpoint', help='calls the url and creates a test with the response. Use `tb test update` to update the contents', type=str)
@click.option('--sql', help='creates a test which runs the SQL, it passes it does not return any row', type=str)
@click.option('--time', help='set max time (ms) to run the test. If the test runs over this time, it fails', type=int)
@click.option('--description', help='set test description', type=str)
@click.option('--enabled', help='', type=bool, default=True)
@click.pass_context
@coro
async def test_add(ctx, file, endpoint, sql, time, description, enabled):
    test_file_add_test(create_tb_client(ctx), file, endpoint, time, description, enabled, sql=sql)


@test.command(name="remove", help="Removes a test from a file.")
@click.option('--file', help='the destination test file. i.e tests/my_test.json', type=str)
@click.option('--id', help='Test identifier', type=int)
@click.pass_context
@coro
async def test_remove(ctx, file, id):
    test_file_remove_test(file, id)


@test.command(name="enable", help="Enables a test from a file.")
@click.option('--file', help='the destination test file. i.e tests/my_test.json', type=str)
@click.option('--id', help='', type=int)
@click.pass_context
@coro
async def test_enable(ctx, file, id):
    test_file_set_test_state(file, id, True)


@test.command(name="disable", help="Disables a test from a file.")
@click.option('--file', help='the destination test file. i.e tests/my_test.json', type=str)
@click.option('--id', help='', type=int)
@click.pass_context
@coro
async def test_disable(ctx, file, id):
    test_file_set_test_state(file, id, False)


@test.command(name="reload", help="Reloads a test or all the tests from a file.")
@click.option('--file', help='the destination test file. i.e tests/my_test.json', type=str)
@click.option('--id', help='', type=int)
@click.pass_context
@coro
async def test_reload(ctx, file, id):
    test_file_reload_test(create_tb_client(ctx), file, id)


@test.command(name="show", help="Show a test from a file.")
@click.option('--file', required=False, help='test file. i.e tests/my_test.json', type=str)
@click.option('--id', help='', type=int)
@click.pass_context
@coro
async def test_show(ctx, file, id):
    if file is None:
        files = glob.glob('tests/*.json')
    else:
        files = [file]

    for x in files:
        test_file_show_test(x, id)
        click.secho('')
        click.secho('')


@test.command(name="run", help="Run the test suite, a file, or a test.")
@click.option('--file', help='the destination test file.', type=str)
@click.option('--id', help='', type=int)
@click.pass_context
@coro
async def test_run(ctx, file, id):
    if ((file is None) and (id is not None)):
        click.echo("Error: Specified test id without test file")
        return
    ctx.exit(tinyUnitRunner(create_tb_client(ctx)))
