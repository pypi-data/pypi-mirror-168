from copy import deepcopy
import logging
import json
from os import environ, getcwd, getenv
import os.path
from enum import Enum
import sys
import shutil
from typing import Any, Dict, List, Optional, Tuple
import uuid
import click
import re
import pprint
from pathlib import Path
from urllib.parse import urlparse

from click import Context
from toposort import toposort
import humanfriendly
import humanfriendly.tables
from tinybird.client import TinyB, AuthException, AuthNoTokenException, CanNotBeDeletedException, DoesNotExistException, OperationCanNotBePerformed, ConnectorNothingToLoad
from sys import version_info
from tinybird.connectors import Connector
from tinybird import context
from tinybird.datafile import (
    folder_push,
    get_name_tag_version,
    parse_pipe,
    parse_datasource,
    ParseException,
    get_project_filenames,
    build_graph,
    format_datasource,
    format_pipe,
    AlreadyExistsException)

from tinybird.feedback_manager import FeedbackManager

import asyncio
import glob
from functools import wraps

from tinybird.config import DEFAULT_LOCALHOST, get_config, write_config, FeatureFlags, VERSION, CURRENT_VERSION, SUPPORTED_CONNECTORS, PROJECT_PATHS, \
    DEFAULT_API_HOST, DEFAULT_UI_HOST

import socket
from contextlib import closing

from tinybird.syncasync import async_to_sync
from tinybird.tb_cli_modules.tinyunit.tinyunit import test_file_add_test, test_file_reload_test, test_file_remove_test, test_file_set_test_state, test_file_show_test, tinyUnitRunner

SUPPORTED_FORMATS = ['csv', 'ndjson', 'json', 'parquet']

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def create_connector(connector: str, options: Dict[str, Any]):
    # Imported here to improve startup time when the connectors aren't used
    from tinybird.connectors import create_connector as _create_connector, UNINSTALLED_CONNECTORS
    if connector in UNINSTALLED_CONNECTORS:
        raise click.ClickException(FeedbackManager.error_connector_not_installed(connector=connector))
    return _create_connector(connector, options)


def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if version_info[1] >= 7:  # FIXME drop python 3.6 support
            return asyncio.run(f(*args, **kwargs))
        else:
            loop = asyncio.get_event_loop()
            return loop.run_until_complete(f(*args, **kwargs))
    return wrapper


def print_data_table(res):
    if not res['data']:
        click.echo(FeedbackManager.info_no_rows())
        return

    dd = []
    for d in res['data']:
        dd.append(d.values())
    click.echo(humanfriendly.tables.format_smart_table(dd, column_names=res['data'][0].keys()))


def normalize_datasource_name(s: str) -> str:
    s = re.sub(r'[^0-9a-zA-Z_]', '_', s)
    if s[0] in '0123456789':
        return "c_" + s
    return s


def generate_datafile(datafile: str, filename: str, data: Optional[bytes], force: bool, _format: str = 'csv'):
    p = Path(filename)
    base = Path('datasources')
    if not base.exists():
        base = Path()
    f = base / (normalize_datasource_name(p.stem) + ".datasource")
    if not f.exists() or force:
        with open(f'{f}', 'w') as ds_file:
            ds_file.write(datafile)
        click.echo(FeedbackManager.success_generated_file(file=f, stem=p.stem, filename=filename))

        if data:
            # generate fixture
            if (base / 'fixtures').exists():
                # Generating a fixture for Parquet files is not so trivial, since Parquet format
                # is column-based. We would need to add PyArrow as a dependency (which is huge)
                # just to analyze the whole Parquet file to extract one single row.
                if _format == 'parquet':
                    click.echo(FeedbackManager.warning_parquet_fixtures_not_supported())
                else:
                    f = base / 'fixtures' / (p.stem + f".{_format}")
                    newline = b'\n'  # TODO: guess
                    with open(f, 'wb') as fixture_file:
                        fixture_file.write(data[:data.rfind(newline)])
                    click.echo(FeedbackManager.success_generated_fixture(fixture=f))
    else:
        click.echo(FeedbackManager.error_file_already_exists(file=f))


async def get_config_and_hosts(ctx: Context) -> Tuple[str, str, str]:
    """Returns (config, host, ui_host)"""

    config = ctx.ensure_object(dict)['config']
    if 'id' not in config:
        config = await _get_config(config['host'], config['token'], load_tb_file=False)

    host = config['host']
    ui_host = DEFAULT_UI_HOST if host == DEFAULT_API_HOST else host

    return config, host, ui_host


async def get_current_workspace(client, config):
    workspaces: List[Dict[str, Any]] = (await client.workspaces()).get('workspaces', [])
    return next((workspace for workspace in workspaces if workspace['id'] == config['id']), None)


class CatchAuthExceptions(click.Group):
    """utility class to get all the auth exceptions"""

    def __call__(self, *args, **kwargs):
        try:
            return self.main(*args, **kwargs)
        except AuthNoTokenException:
            click.echo(FeedbackManager.error_notoken())
        except AuthException as exc:
            click.echo(FeedbackManager.error_exception(error=exc))


def load_connector_config(ctx: Context, connector_name: str, debug: bool, check_uninstalled: bool = False):
    config_file = Path(getcwd()) / f".tinyb_{connector_name}"
    try:
        if connector_name not in ctx.ensure_object(dict):
            with open(config_file) as file:
                config = json.loads(file.read())
            from tinybird.connectors import UNINSTALLED_CONNECTORS
            if check_uninstalled and connector_name in UNINSTALLED_CONNECTORS:
                click.echo(FeedbackManager.warning_connector_not_installed(connector=connector_name))
                return
            ctx.ensure_object(dict)[connector_name] = create_connector(connector_name, config)
    except IOError:
        if debug:
            click.echo(f"** {connector_name} connector not configured")
        pass


def create_tb_client(ctx: Context) -> TinyB:
    token = ctx.ensure_object(dict)['config'].get('token', '')
    host = ctx.ensure_object(dict)['config'].get('host', DEFAULT_API_HOST)
    return TinyB(token, host, version=VERSION)


@click.group(cls=CatchAuthExceptions)  # noqa: C901
@click.option('--debug/--no-debug', default=False, help="Prints internal representation, can be combined with any command to get more information.")
@click.option('--token', envvar='TB_TOKEN', help="Use auth token, defaults to TB_TOKEN envvar, then to the .tinyb file")
@click.option('--host', envvar='TB_HOST', help="Use custom host, defaults to TB_HOST envvar, then to https://api.tinybird.co")
@click.option('--gcp-project-id', help="The Google Cloud project ID", hidden=True)
@click.option('--gcs-bucket', help="The Google Cloud Storage bucket to write temp files when using the connectors", hidden=True)
@click.option('--google-application-credentials', envvar='GOOGLE_APPLICATION_CREDENTIALS', help="Set GOOGLE_APPLICATION_CREDENTIALS", hidden=True)
@click.option('--sf-account', help="The Snowflake Account (e.g. your-domain.west-europe.azure)", hidden=True)
@click.option('--sf-warehouse', help="The Snowflake warehouse name", hidden=True)
@click.option('--sf-database', help="The Snowflake database name", hidden=True)
@click.option('--sf-schema', help="The Snowflake schema name", hidden=True)
@click.option('--sf-role', help="The Snowflake role name", hidden=True)
@click.option('--sf-user', help="The Snowflake user name", hidden=True)
@click.option('--sf-password', help="The Snowflake password", hidden=True)
@click.option('--sf-storage-integration', help="The Snowflake GCS storage integration name (leave empty to auto-generate one)", hidden=True)
@click.option('--sf-stage', help="The Snowflake GCS stage name (leave empty to auto-generate one)", hidden=True)
@click.option('--with-headers', help="Flag to enable connector to export with headers", is_flag=True, default=False, hidden=True)
@click.option('--version-warning/--no-version-warning', envvar='TB_VERSION_WARNING', default=True, help="Don't print version warning message if there's a new available version. You can use TB_VERSION_WARNING envar")
@click.version_option(version=VERSION)
@click.pass_context
@coro
async def cli(ctx: Context, debug: bool, token: str, host: str, gcp_project_id, gcs_bucket, google_application_credentials, sf_account, sf_warehouse, sf_database, sf_schema, sf_role, sf_user, sf_password, sf_storage_integration, sf_stage, with_headers: bool, version_warning: bool):  # noqa: C901
    # ensure that ctx.obj exists and is a dict (in case `cli()` is called)
    # by means other than the `if` block below
    if not environ.get("PYTEST", None) and version_warning and not token:
        from tinybird.check_pypi import CheckPypi
        latest_version = await CheckPypi().get_latest_version()

        if 'x.y.z' in CURRENT_VERSION:
            click.echo(FeedbackManager.warning_development_cli())

        if 'x.y.z' not in CURRENT_VERSION and latest_version != CURRENT_VERSION:
            click.echo(FeedbackManager.warning_update_version(latest_version=latest_version))
            click.echo(FeedbackManager.warning_current_version(current_version=CURRENT_VERSION))

    if debug:
        logging.basicConfig(level=logging.DEBUG)

    config = await get_config(host, token)
    ctx.ensure_object(dict)['config'] = config

    if ctx.invoked_subcommand == 'auth':
        return

    if gcp_project_id and gcs_bucket and google_application_credentials and not sf_account:
        bq_config = {
            'project_id': gcp_project_id,
            'bucket_name': gcs_bucket,
            'service_account': google_application_credentials,
            'with_headers': with_headers
        }
        ctx.ensure_object(dict)['bigquery'] = create_connector('bigquery', bq_config)
    if sf_account and sf_warehouse and sf_database and sf_schema and sf_role and sf_user and sf_password and gcs_bucket and google_application_credentials and gcp_project_id:
        sf_config = {
            'account': sf_account,
            'warehouse': sf_warehouse,
            'database': sf_database,
            'schema': sf_schema,
            'role': sf_role,
            'user': sf_user,
            'password': sf_password,
            'storage_integration': sf_storage_integration,
            'stage': sf_stage,
            'bucket_name': gcs_bucket,
            'service_account': google_application_credentials,
            'project_id': gcp_project_id,
            'with_headers': with_headers
        }
        ctx.ensure_object(dict)['snowflake'] = create_connector('snowflake', sf_config)

    logging.debug("debug enabled")

    ctx.ensure_object(dict)['client'] = TinyB(config.get('token', None), config['host'], version=VERSION)

    for connector in SUPPORTED_CONNECTORS:
        load_connector_config(ctx, connector, debug, check_uninstalled=True)


async def _analyze(filename: str, client: TinyB, format: str, connector: Optional[Connector] = None):
    data: Optional[bytes] = None
    if not connector:
        parsed = urlparse(filename)
        if parsed.scheme in ('http', 'https'):
            meta = await client.datasource_analyze(filename)
        else:
            with open(filename, 'rb') as file:
                # We need to read the whole file in binary for Parquet, while for the
                # others we just read 1KiB
                if format == 'parquet':
                    data = file.read()
                else:
                    data = file.read(1024 * 1024)

            meta = await client.datasource_analyze_file(data)
    else:
        meta = connector.datasource_analyze(filename)
    return meta, data


async def _generate_datafile(filename: str, client: TinyB, force: bool, format: str, connector: Optional[Connector] = None):
    meta, data = await _analyze(filename, client, format, connector=connector)
    schema = meta['analysis']['schema']
    schema = schema.replace(', ', ',\n    ')
    datafile = f"""DESCRIPTION >\n    Generated from {filename}\n\nSCHEMA >\n    {schema}"""
    return generate_datafile(datafile, filename, data, force, _format=format)


async def folder_init(client, folder, generate_datasources=False, force=False):
    for x in PROJECT_PATHS:
        try:
            f = Path(folder) / x
            f.mkdir()
            click.echo(FeedbackManager.info_path_created(path=x))
        except FileExistsError:
            if not force:
                click.echo(FeedbackManager.info_path_already_exists(path=x))
            pass

    if generate_datasources:
        for format in SUPPORTED_FORMATS:
            for path in Path(folder).glob(f'*.{format}'):
                await _generate_datafile(str(path), client, format=format, force=force)


@cli.command()
@click.option('--generate-datasources', is_flag=True, default=False, help="Generate datasources based on CSV, NDJSON and Parquet files in this folder")
@click.option('--folder', default=None, type=click.Path(exists=True, file_okay=False), help="Folder where files will be placed")
@click.option('--force', is_flag=True, default=False, help="Overrides existing files")
@click.pass_context
@coro
async def init(ctx, generate_datasources, folder, force):
    """Initialize folder layout"""
    client = ctx.obj['client']
    folder = folder if folder else getcwd()
    await folder_init(client, folder, generate_datasources, force=force)
    return


@cli.command()
@click.argument('filename', type=click.Path(exists=True))
@click.option('--debug', is_flag=True, default=False, help="Print internal representation")
def check(filename, debug):
    """Check file syntax"""
    click.echo(FeedbackManager.info_processing_file(filename=filename))

    try:
        if '.pipe' in filename:
            doc = parse_pipe(filename)
        else:
            doc = parse_datasource(filename)

        click.echo(FeedbackManager.success_processing_file(filename=filename))

    except ParseException as e:
        raise click.ClickException(FeedbackManager.error_exception(error=e))

    if debug:
        pp = pprint.PrettyPrinter()
        for x in doc.nodes:
            pp.pprint(x)


@cli.command()
@click.option('--prefix', default='', help="Use prefix for all the resources")
@click.option('--dry-run', is_flag=True, default=False, help="Run the command without creating resources on the Tinybird account or any side effect")
@click.option('--check/--no-check', is_flag=True, default=True, help="Enable/Disable output checking, enabled by default")
@click.option('--push-deps', is_flag=True, default=False, help="Push dependencies, disabled by default")
@click.option('--debug', is_flag=True, default=False, help="Prints internal representation, can be combined with any command to get more information.")
@click.option('-f', '--force', is_flag=True, default=False, help="Override pipes when they already exist")
@click.option('--override-datasource', is_flag=True, default=False, help="When pushing a pipe with a Materialized node if the target Data Source exists it will try to override it.")
@click.option('--populate', is_flag=True, default=False, help="Populate materialized nodes when pushing them")
@click.option('--subset', type=float, default=None, help="Populate with a subset percent of the data (limited to a maximum of 2M rows), this is useful to quickly test a materialized node with some data. The subset must be greater than 0 and lower than 0.1. A subset of 0.1 means a 10 percent of the data in the source Data Source will be used to populate the materialized view. Use it together with --populate, it has precedence over --sql-condition")
@click.option('--sql-condition', type=str, default=None, help="Populate with a SQL condition to be applied to the trigger Data Source of the Materialized View. For instance, `--sql-condition='date == toYYYYMM(now())'` it'll populate taking all the rows from the trigger Data Source which `date` is the current month. Use it together with --populate. --sql-condition is not taken into account if the --subset param is present. Including in the ``sql_condition`` any column present in the Data Source ``engine_sorting_key`` will make the populate job process less data.")
@click.option('--fixtures', is_flag=True, default=False, help="Append fixtures to data sources")
@click.option('--wait', is_flag=True, default=False, help="To be used along with --populate command. Waits for populate jobs to finish, showing a progress bar. Combined with --debug, displays the estimated remaining job times.")
@click.option('--yes', is_flag=True, default=False, help="Do not ask for confirmation")
@click.option('--only-response-times', is_flag=True, default=False, help="Checks only response times, when --force push a pipe")
@click.argument('filenames', type=click.Path(exists=True), nargs=-1, default=None)
@click.option('--workspace_map', nargs=2, type=str, multiple=True)
@click.option('--workspace', nargs=2, type=str, multiple=True, help="add a workspace path to the list of external workspaces, usage: --workspace name path/to/folder")
@click.option('--no-versions', is_flag=True, default=False, help="when set, resource dependency versions are not used, it pushes the dependencies as-is")
@click.option('--timeout', type=float, default=None, help="timeout you want to use for the job populate")
@click.option('-l', '--limit', type=click.IntRange(0, 100), default=0, required=False, help="Number of requests to validate")
@click.option('--sample-by-params', type=click.IntRange(1, 100), default=1, required=False, help="When set, we will aggregate the pipe_stats_rt requests by extractURLParameterNames(assumeNotNull(url)) and for each combination we will take a sample of N requests")
@click.option('-ff', '--failfast', is_flag=True, default=False, help="When set, the checker will exit as soon one test fails")
@click.option('--ignore-order', is_flag=True, default=False, help="When set, the checker will ignore the order of list properties")
@click.pass_context
@coro
async def push(
    ctx: click.Context,
    prefix: str,
    filenames: Path,
    dry_run: bool,
    check: bool,
    push_deps: bool,
    debug: bool,
    force: bool,
    override_datasource: bool,
    populate: bool,
    subset: Optional[float],
    sql_condition: Optional[str],
    fixtures: bool,
    wait: bool,
    yes: bool,
    only_response_times: bool,
    workspace_map,
    workspace,
    no_versions: bool,
    timeout: Optional[float],
    limit: int,
    sample_by_params: int,
    failfast: bool,
    ignore_order: bool
):

    """Push files to Tinybird
    """

    ignore_sql_errors = FeatureFlags.ignore_sql_errors()
    context.disable_template_security_validation.set(True)
    await folder_push(
        create_tb_client(ctx),
        prefix,
        filenames,
        dry_run,
        check,
        push_deps,
        debug,
        force,
        override_datasource=override_datasource,
        populate=populate,
        populate_subset=subset,
        populate_condition=sql_condition,
        upload_fixtures=fixtures,
        wait=wait,
        ignore_sql_errors=ignore_sql_errors,
        skip_confirmation=yes,
        only_response_times=only_response_times,
        workspace_map=dict(workspace_map),
        workspace_lib_paths=workspace,
        no_versions=no_versions,
        timeout=timeout,
        run_tests=False,
        tests_to_run=limit,
        tests_sample_by_params=sample_by_params,
        tests_failfast=failfast,
        tests_ignore_order=ignore_order
    )
    return


@cli.command()  # noqa: C901
@click.option('--folder', default=None, type=click.Path(exists=True, file_okay=False), help="Folder where files will be placed")
@click.option('--auto', is_flag=True, default=False, help="Saves datafiles automatically into their default directories (/datasources or /pipes)")
@click.option('--match', default=None, help='Retrieve any resourcing matching the pattern. eg --match _test')
@click.option('--prefix', default=None, help="Download only resources with this prefix")
@click.option('--force', is_flag=True, default=False, help="Override existing files")
@click.pass_context
@coro
async def pull(ctx, folder, auto, match, prefix, force):
    """Retrieve latest versions for project files from Tinybird"""
    client = ctx.obj['client']
    folder = folder if folder else getcwd()

    return await folder_pull(client, folder, auto, match, prefix, force)


async def folder_pull(client, folder, auto, match, tag, force):  # noqa: C901
    pattern = re.compile(match) if match else None

    def _get_latest_versions(resources, tag):
        versions = {}

        for x in resources:
            t = get_name_tag_version(x)
            t['original_name'] = x
            if t['version'] is None:
                t['version'] = -1
            name = t['name']

            if not tag:
                versions[name] = t
            elif t['tag'] == tag:
                if name in versions:
                    if versions[name]['version'] < t['version']:
                        versions[name] = t
                else:
                    versions[name] = t
        return versions

    def get_file_folder(extension):
        if not auto:
            return None
        if extension == 'datasource':
            return 'datasources'
        if extension == 'pipe':
            return 'pipes'
        return None

    async def write_files(versions, resources, extension, get_resource_function):
        values = versions.values()

        for k in values:
            name = f"{k['name']}.{extension}"

            prefix_info = ''
            prefix_name = ''
            if not tag:
                if k['tag']:
                    prefix_name = f"{k['tag']}"
                    prefix_info = f"({prefix_name})"
            else:
                prefix_name = f"{tag}"
                prefix_info = f"({prefix_name})"

            try:
                if pattern and not pattern.search(name):
                    click.echo(FeedbackManager.info_skipping_resource(resource=name))
                    continue

                resource = await getattr(client, get_resource_function)(k['original_name'])

                dest_folder = folder
                if '.' in k['name']:
                    dest_folder = Path(folder) / 'vendor' / k['name'].split('.', 1)[0]
                    name = f"{k['name'].split('.', 1)[1]}.{extension}"

                file_folder = get_file_folder(extension)
                f = Path(dest_folder) / file_folder if file_folder is not None else Path(dest_folder)

                if not f.exists():
                    f.mkdir(parents=True)

                f = f / name

                click.echo(FeedbackManager.info_writing_resource(resource=f, prefix=prefix_info))
                if not f.exists() or force:
                    with open(f, 'w') as fd:
                        # versions are a client only thing so
                        # datafiles from the server do not contains information about versions
                        if k['version'] >= 0:
                            resource = f"VERSION {k['version']}\n" + resource
                        if resource:
                            matches = re.findall(rf'(({prefix_name}__)?([^\s\.]*)__v\d+)', resource)
                            for match in set(matches):
                                if match[2] in resources:
                                    resource = resource.replace(match[0], match[2])
                            fd.write(resource)
                else:
                    click.echo(FeedbackManager.info_skip_already_exists())
            except Exception as e:
                raise Exception(FeedbackManager.error_exception(error=e))
        return

    try:
        datasources = await client.datasources()
        remote_datasources = sorted([x['name'] for x in datasources])
        datasources_versions = _get_latest_versions(remote_datasources, tag)

        pipes = await client.pipes()
        remote_pipes = sorted([x['name'] for x in pipes])
        pipes_versions = _get_latest_versions(remote_pipes, tag)

        resources = list(datasources_versions.keys()) + list(pipes_versions.keys())

        await write_files(datasources_versions, resources, 'datasource', 'datasource_file')
        await write_files(pipes_versions, resources, 'pipe', 'pipe_file')

        return

    except Exception as e:
        raise click.ClickException(FeedbackManager.error_pull(error=str(e)))


@cli.command()
@click.option('--no-deps', is_flag=True, default=False, help="Print only data sources with no pipes using them")
@click.option('--match', default=None, help='Retrieve any resource matching the pattern')
@click.option('--pipe', default=None, help='Retrieve any resource used by pipe')
@click.option('--datasource', default=None, help='Retrieve resources depending on this Data Source')
@click.option('--check-for-partial-replace', is_flag=True, default=False, help='Retrieve dependant Data Sources that will have their data replaced if a partial replace is executed in the Data Source selected')
@click.option('--recursive', is_flag=True, default=False, help='Calculate recursive dependencies')
@click.pass_context
@coro
async def dependencies(ctx, no_deps, match, pipe, datasource, check_for_partial_replace, recursive):
    """
    Print all data sources dependencies
    """
    client = ctx.obj['client']

    response = await client.datasource_dependencies(no_deps, match, pipe, datasource, check_for_partial_replace, recursive)
    for ds in response['dependencies']:
        click.echo(FeedbackManager.info_dependency_list(dependency=ds))
        for pipe in response['dependencies'][ds]:
            click.echo(FeedbackManager.info_dependency_list_item(dependency=pipe))
    if 'incompatible_datasources' in response and len(response['incompatible_datasources']):
        click.echo(FeedbackManager.info_no_compatible_dependencies_found())
        for ds in response['incompatible_datasources']:
            click.echo(FeedbackManager.info_dependency_list(dependency=ds))
        raise click.ClickException(
            FeedbackManager.error_partial_replace_cant_be_executed(datasource=datasource))


@cli.command()
@click.argument('filenames', type=click.Path(exists=True), nargs=-1, required=True)
@click.option('--line-length', is_flag=False, default=100, help="A number indicating the maximum characters per line in the node SQL, lines will be splitted based on the SQL syntax and the number of characters passed as a parameter")
@click.option('--dry-run', is_flag=True, default=False, help="Don't ask to override the local file")
@click.option('--yes', is_flag=True, default=False, help="Do not ask for confirmation to overwrite the local file")
@click.pass_context
@coro
async def fmt(ctx, filenames, line_length: int, dry_run: bool, yes: bool):
    """
    Formats a .datasource, .pipe or .incl file

    This command removes comments starting with # from the file, use DESCRIPTION instead.

    The format command tries to parse the datafile so syntax errors might rise.

    .incl files must contain a NODE definition
    """
    result = ''
    for filename in filenames:
        extension = Path(filename).suffix
        if extension == '.datasource':
            result = format_datasource(filename)
        elif extension in ['.pipe', '.incl']:
            result = format_pipe(filename, line_length)
        else:
            click.echo("Unsupported file type")
            return

        click.echo(result)
        if dry_run:
            return

        if yes or click.confirm(FeedbackManager.prompt_override_local_file(name=filename)):
            with open(f'{filename}', 'w') as file:
                file.write(result)

            click.echo(FeedbackManager.success_generated_local_file(file=filename))

    return result


async def configure_connector(connector):
    if connector not in SUPPORTED_CONNECTORS:
        click.echo(FeedbackManager.error_invalid_connector(connectors=', '.join(SUPPORTED_CONNECTORS)))
        return

    file_name = f".tinyb_{connector}"
    config_file = Path(getcwd()) / file_name
    if connector == 'bigquery':
        project = click.prompt("BigQuery project ID")
        service_account = click.prompt("Path to a JSON service account file with permissions to export from BigQuery, write in Storage and sign URLs (leave empty to use GOOGLE_APPLICATION_CREDENTIALS environment variable)", default=environ.get('GOOGLE_APPLICATION_CREDENTIALS', ''))
        bucket_name = click.prompt("Name of a Google Cloud Storage bucket to store temporary exported files")

        try:
            config = {
                'project_id': project,
                'service_account': service_account,
                'bucket_name': bucket_name
            }
            await write_config(config, file_name)
        except Exception:
            raise click.ClickException(FeedbackManager.error_file_config(config_file=config_file))
    elif connector == 'snowflake':
        sf_account = click.prompt("Snowflake Account (e.g. your-domain.west-europe.azure)")
        sf_warehouse = click.prompt("Snowflake warehouse name")
        sf_database = click.prompt("Snowflake database name")
        sf_schema = click.prompt("Snowflake schema name")
        sf_role = click.prompt("Snowflake role name")
        sf_user = click.prompt("Snowflake user name")
        sf_password = click.prompt("Snowflake password")
        sf_storage_integration = click.prompt("Snowflake GCS storage integration name (leave empty to auto-generate one)", default='')
        sf_stage = click.prompt("Snowflake GCS stage name (leave empty to auto-generate one)", default='')
        project = click.prompt("Google Cloud project ID to store temporary files")
        service_account = click.prompt("Path to a JSON service account file with permissions to write in Storagem, sign URLs and IAM (leave empty to use GOOGLE_APPLICATION_CREDENTIALS environment variable)", default=environ.get('GOOGLE_APPLICATION_CREDENTIALS', ''))
        bucket_name = click.prompt("Name of a Google Cloud Storage bucket to store temporary exported files")

        if not service_account:
            service_account = getenv('GOOGLE_APPLICATION_CREDENTIALS')

        try:
            config = {
                'account': sf_account,
                'warehouse': sf_warehouse,
                'database': sf_database,
                'schema': sf_schema,
                'role': sf_role,
                'user': sf_user,
                'password': sf_password,
                'storage_integration': sf_storage_integration,
                'stage': sf_stage,
                'service_account': service_account,
                'bucket_name': bucket_name,
                'project_id': project,
            }
            await write_config(config, file_name)
        except Exception:
            raise click.ClickException(FeedbackManager.error_file_config(config_file=config_file))

        click.echo(FeedbackManager.success_connector_config(connector=connector, file_name=file_name))


@cli.group(invoke_without_command=True)
@click.option('--token', envvar='TB_TOKEN', help="Use auth token, defaults to TB_TOKEN envvar, then to the .tinyb file")
@click.option('--host', envvar='TB_HOST', help="Set custom host if it's different than https://api.tinybird.co. Check https://docs.tinybird.co/cli.html for the available list of regions")
@click.option('--region', envvar='TB_REGION', help="Set region. Run 'tb auth ls' to show available regions")
@click.option('--connector', type=click.Choice(['bigquery', 'snowflake'], case_sensitive=True), help="Set credentials for one of the supported connectors")
@click.option('-i', '--interactive', is_flag=True, default=False, help="Show available regions and select where to authenticate to")
@click.pass_context
@coro
async def auth(ctx: Context, token: str, host: str, region: str, connector: str, interactive: bool):
    """Configure auth"""
    if connector:
        await configure_connector(connector)
        return

    # only run when doing 'tb auth'
    if not ctx.invoked_subcommand:
        regions = None

        if region:
            regions, host = await get_host_from_region(region, host)

        config = None

        try:
            config = await authenticate(ctx, host=host, token=token, regions=regions, interactive=interactive, try_all_regions=True)
        except Exception as e:
            raise click.ClickException(FeedbackManager.error_exception(error=str(e)))

        if not config:
            raise click.ClickException(FeedbackManager.error_auth())

    elif ctx.invoked_subcommand == 'ls':
        pass

    else:
        config = None
        try:
            config_file = Path(getcwd()) / ".tinyb"
            with open(config_file) as file:
                config = json.loads(file.read())
            ctx.ensure_object(dict)['client'] = TinyB(config['token'], config.get('host', DEFAULT_API_HOST), version=VERSION)
            ctx.ensure_object(dict)['config'] = config
        except Exception:
            host = ctx.ensure_object(dict)['config'].get('host', DEFAULT_API_HOST)
            token = ctx.ensure_object(dict)['config']['token']

            if not token:
                raise click.ClickException(FeedbackManager.error_notoken())

            config = await _get_config(host, token)
            ctx.ensure_object(dict)['config'] = config

        if not config or not config['token']:
            raise click.ClickException(FeedbackManager.error_wrong_config_file(config_file=config_file))


async def _get_config(host, token, load_tb_file=True):
    config = {}

    try:
        client = TinyB(token, host, version=VERSION)
        response = await client.workspace_info()
    except Exception:
        raise click.ClickException(FeedbackManager.error_invalid_token_for_host(host=host))

    from_response = load_tb_file

    try:
        config_file = Path(getcwd()) / ".tinyb"
        with open(config_file) as file:
            config = json.loads(file.read())
    except Exception:
        from_response = True

    if not from_response:
        return config

    config.update({
        'host': host,
        'token': token,
        'id': response['id'],
        'name': response['name']
    })

    if 'user_email' in response:
        config['user_email'] = response['user_email']
    if 'user_id' in response:
        config['user_id'] = response['user_id']
    if 'scope' in response:
        config['scope'] = response['scope']
    if 'id' in response:
        config['id'] = response['id']

    tokens = config.get('tokens', {})

    tokens.update({host: token})
    config['tokens'] = tokens
    config['token'] = tokens[host]
    config['host'] = host

    return config


@auth.command(name="info")
@click.pass_context
@coro
async def auth_info(ctx):
    """Get information about the authentication that is currently being used"""
    config = ctx.obj['config']

    if config and 'id' in config:
        columns = ['user', 'host', 'workspace_name', 'workspace_id']
        table = []
        user_email = config['user_email'] if 'user_email' in config else None

        if user_email:
            table.append([user_email, config['host'], config['name'], config['id']])
        else:
            table.append(['No user', config['host'], config['name'], config['id']])
        print(humanfriendly.tables.format_smart_table(table, column_names=columns))


async def get_regions(client: TinyB, config_file: Path) -> List[Dict[str, str]]:
    regions: List[Dict[str, str]] = []
    try:
        response = await client.regions()
        regions = response['regions']
    except Exception:
        pass

    try:
        with open(config_file) as file:
            config = json.loads(file.read())
            if 'tokens' not in config:
                return regions

            for key in config['tokens']:
                region = next((region for region in regions if key == region['api_host'] or key == region['host']), None)
                if region:
                    region['default_password'] = config['tokens'][key]
                else:
                    regions.append({
                        'api_host': key,
                        'host': key,
                        'name': key,
                        'default_password': config['tokens'][key]
                    })

    except Exception:
        pass

    return regions


@auth.command(name="ls")
@click.pass_context
@coro
async def auth_ls(ctx: Context):
    """List available regions to authenticate"""
    config = ctx.ensure_object(dict)['config']

    config_file = Path(getcwd()) / ".tinyb"
    is_localhost = FeatureFlags.is_localhost()
    check_host = config.get('host', DEFAULT_API_HOST)
    check_host = check_host if not is_localhost else DEFAULT_LOCALHOST
    client = TinyB(token='', host=check_host, version=VERSION)

    columns = ['idx', 'region', 'host', 'api', 'current']
    table = []
    click.echo(FeedbackManager.info_available_regions())

    regions = await get_regions(client, config_file)

    if regions:
        for index, region in enumerate(regions):
            table.append([index + 1, region['name'].lower(), region['host'], region['api_host'], _compare_hosts(region, config)])
    else:
        table.append([1, 'default', config['host'], True])

    print(humanfriendly.tables.format_smart_table(table, column_names=columns))


def _compare_hosts(region: Dict[str, Any], config: Dict[str, Any]) -> bool:
    return region['host'] == config['host'] or region['api_host'] == config['host']


@auth.command(name="use")
@click.argument('region_name_or_host_or_id')
@click.pass_context
@coro
async def auth_use(ctx, region_name_or_host_or_id):
    """Switch to a different region.
    You can pass the region name, the region host url, or the region index
    after listing available regions with 'tb auth ls'

    \b
    Example usage:
    \b
    $ tb auth use us-east
    $ tb auth use 1
    $ tb auth use https://ui.us-east.tinybird.co
    """

    config = ctx.obj['config']
    token = None
    host = config.get('host', None)

    regions, host = await get_host_from_region(region_name_or_host_or_id, host)

    if 'tokens' in config and host in config['tokens']:
        token = config['tokens'][host]

    config = await authenticate(ctx, host, token, regions)

    await write_config(config)
    click.echo(FeedbackManager.success_now_using_config(name=config['name'], id=config['id']))


async def get_host_from_region(region_name_or_host_or_id: str, host: Optional[str] = None):
    is_localhost = FeatureFlags.is_localhost()

    if not host:
        host = DEFAULT_API_HOST if not is_localhost else DEFAULT_LOCALHOST

    client = TinyB(token='', host=host, version=VERSION)

    try:
        response = await client.regions()
        regions = response['regions']
    except Exception:
        regions = []

    if not regions:
        click.echo(f"No regions available, using host: {host}")
        return [], host

    try:
        index = int(region_name_or_host_or_id)
        try:
            host = regions[index - 1]['api_host']
        except Exception:
            raise click.ClickException(FeedbackManager.error_getting_region_by_index())
    except Exception:
        region_name_or_host_or_id = region_name_or_host_or_id.lower()
        try:
            region = next((region for region in regions if _compare_region_host(region_name_or_host_or_id, region)), None)
            host = region['api_host'] if region else None
        except Exception:
            raise click.ClickException(FeedbackManager.error_getting_region_by_name_or_url())

    if not host:
        raise click.ClickException(FeedbackManager.error_getting_region_by_name_or_url())

    return regions, host


def _compare_region_host(region_name_or_host: str, region: Dict[str, Any]) -> bool:
    if region['name'].lower() == region_name_or_host:
        return True
    if region['host'] == region_name_or_host:
        return True
    if region['api_host'] == region_name_or_host:
        return True
    return False


def ask_for_region_interactively(regions):
    region_index = -1

    while region_index == -1:
        click.echo(FeedbackManager.info_available_regions())
        for index, region in enumerate(regions):
            click.echo(f"   [{index + 1}] {region['name'].lower()} ({region['host']})")
        click.echo("   [0] Cancel")

        region_index = click.prompt("\nUse region", default=1)

        if region_index == 0:
            click.echo(FeedbackManager.info_auth_cancelled_by_user())
            return None

        try:
            return regions[int(region_index) - 1]
        except Exception:
            available_options = ', '.join(map(str, range(1, len(regions) + 1)))
            click.echo(FeedbackManager.error_region_index(host_index=region_index, available_options=available_options))
            region_index = -1


def get_region_info(ctx, region=None):
    is_localhost = FeatureFlags.is_localhost()

    name = region['name'] if region else 'default'
    host = region['api_host'] or region['host'] if region else ctx.obj['config'].get('host', DEFAULT_API_HOST)

    if 'localhost' in host or is_localhost:
        ui_host = f'http://{host}' if 'http' not in host else host
        host = ui_host
    elif not host.startswith('http'):
        ui_host = DEFAULT_UI_HOST if host == DEFAULT_API_HOST else host
        ui_host = f'https://{ui_host}'
    else:
        ui_host = DEFAULT_UI_HOST if host == DEFAULT_API_HOST else host

    return name, host, ui_host


def region_from_host(region_name_or_host, regions):
    """Returns the region that matches region_name_or_host"""

    return next((r for r in regions if _compare_region_host(region_name_or_host, r)), None)


async def try_get_config(host, token):
    try:
        return await _get_config(host, token)
    except Exception:
        return None


async def authenticate(ctx, host, token=None, regions=None, interactive=False, try_all_regions=False):
    is_localhost = FeatureFlags.is_localhost()
    check_host = DEFAULT_API_HOST if not host and not is_localhost else DEFAULT_LOCALHOST

    client = TinyB(token='', host=check_host, version=VERSION)
    config_file = Path(getcwd()) / ".tinyb"
    default_password: Optional[str] = None

    if not regions and interactive:
        regions = await get_regions(client, config_file)

    selected_region = None

    if regions and interactive:
        selected_region = ask_for_region_interactively(regions)
        if selected_region is None:
            return None

        host = selected_region['api_host']
        default_password = selected_region.get('default_password', None)
    elif regions and not interactive:
        selected_region = region_from_host(host, regions)

    if host and not regions and not selected_region:
        name, host, ui_host = (host, host, host)
    else:
        name, host, ui_host = get_region_info(ctx, selected_region)

    token = token or ctx.ensure_object(dict)['config'].get('token_passed')

    if not token:
        token = click.prompt(
            f"\nCopy the admin token from {ui_host}/tokens and paste it here { f'OR press enter to use the token from .tinyb file' if default_password else ''}",
            hide_input=True,
            show_default=False,
            default=default_password)

    config = await try_get_config(host, token)
    if config is None and not try_all_regions:
        raise click.ClickException(FeedbackManager.error_invalid_token_for_host(host=host))

    # No luck? Let's try auth in all other regions
    if config is None and try_all_regions and not interactive:
        if not regions:
            regions = await get_regions(client, config_file)

        # Check other regions, ignoring the previously tested region
        for region in [r for r in regions if r is not selected_region]:
            name, host, ui_host = get_region_info(ctx, region)
            config = await try_get_config(host, token)
            if config is not None:
                click.echo(FeedbackManager.success_using_host(name=name, host=ui_host))
                break

    if config is None:
        raise click.ClickException(FeedbackManager.error_invalid_token())

    try:
        if 'id' in config:
            await write_config(config)
            ctx.ensure_object(dict)['client'] = TinyB(config['token'], config.get('host', DEFAULT_API_HOST), version=VERSION)
            ctx.ensure_object(dict)['config'] = config
        else:
            raise click.ClickException(FeedbackManager.error_not_personal_auth())
    except Exception as e:
        raise click.ClickException(FeedbackManager.error_exception(error=str(e)))

    click.echo(FeedbackManager.success_auth())
    click.echo(FeedbackManager.success_remember_api_host(host=config['host']))

    if 'scope' not in config or not config['scope']:
        click.echo(FeedbackManager.warning_token_scope())

    if 'scope' in config and config['scope'] == 'admin':
        click.echo(FeedbackManager.warning_workspaces_admin_token())

    return config


@cli.group()
@click.pass_context
def workspace(ctx):
    '''Workspace commands'''


@workspace.command(name="ls")
@click.pass_context
@coro
async def workspace_ls(ctx):
    """List all the workspaces you have access to in the account you're currently authenticated to
    """

    client = ctx.obj['client']
    config = ctx.obj['config']

    if 'id' not in config:
        config = await _get_config(config['host'], config['token'], load_tb_file=False)

    response = await client.workspaces()

    if 'scope' in response and response['scope'] == 'admin':
        click.echo(FeedbackManager.warning_workspaces_admin_token())

    columns = ['name', 'id', 'role', 'plan', 'current']
    table = []
    click.echo(FeedbackManager.info_workspaces())

    for workspace in response['workspaces']:
        table.append([workspace['name'], workspace['id'], workspace['role'], _get_workspace_plan_name(workspace['plan']), config['id'] == workspace['id']])

    print(humanfriendly.tables.format_smart_table(table, column_names=columns))


@workspace.command(name='use')
@click.argument('workspace_name_or_id')
@click.pass_context
@coro
async def workspace_use(ctx: Context, workspace_name_or_id: str):
    """Switch to another workspace. Use 'tb workspace ls' to list the workspaces you have access to.
    """

    config_file = Path(getcwd()) / ".tinyb"
    config = {}
    client: TinyB = ctx.ensure_object(dict)['client']
    config = ctx.ensure_object(dict)['config']

    try:
        if 'id' not in config:
            config = await _get_config(config['host'], config['token'], load_tb_file=False)
        else:
            with open(config_file) as file:
                config = json.loads(file.read())

        response = await client.workspaces()

        workspaces = response['workspaces']
        workspace = next((workspace for workspace in workspaces if workspace['name'] == workspace_name_or_id or workspace['id'] == workspace_name_or_id), None)

        if not workspace:
            click.echo(FeedbackManager.error_workspace(workspace=workspace_name_or_id))
            return

        client = TinyB(workspace['token'], config['host'], version=VERSION)

        config['id'] = workspace['id']
        config['name'] = workspace['name']
        config['token'] = workspace['token']
        host = config['host']

        tokens = config.get('tokens', {})
        tokens[host] = config['token']

        config['tokens'] = tokens

        ctx.ensure_object(dict)['client'] = client
        ctx.ensure_object(dict)['config'] = config

        await write_config(config)
        click.echo(FeedbackManager.success_now_using_config(name=config['name'], id=config['id']))
    except Exception as e:
        click.echo(FeedbackManager.error_exception(error=str(e)))
        return


@workspace.command(name='current')
@click.pass_context
@coro
async def workspace_current(ctx: Context):
    """Show the workspace you're currently authenticated to
    """

    client: TinyB = ctx.ensure_object(dict)['client']
    config = ctx.ensure_object(dict)['config']

    if 'id' not in config:
        config = await _get_config(config['host'], config['token'], load_tb_file=False)

    response = await client.workspaces()

    columns = ['name', 'id', 'role', 'plan', 'current']
    table = []
    click.echo(FeedbackManager.info_current_workspace())

    for workspace in response['workspaces']:
        if config['id'] == workspace['id']:
            table.append([workspace['name'], workspace['id'], workspace['role'], _get_workspace_plan_name(workspace['plan']), True])

    print(humanfriendly.tables.format_smart_table(table, column_names=columns))


@workspace.command(name='clear', short_help="Drop all the resources inside a project. This command is dangerous because it removes everything, use with care.")
@click.option('--yes', is_flag=True, default=False, help="Do not ask for confirmation")
@click.option('--dry-run', is_flag=True, default=False, help="Run the command without removing anything")
@click.pass_context
@coro
async def clear_workspace(ctx: Context, yes: bool, dry_run: bool):
    """Drop all the resources inside a project. This command is dangerous because it removes everything, use with care"""

    """ Get current workspace to add the name to the alert message"""
    client: TinyB = ctx.ensure_object(dict)['client']
    config = ctx.ensure_object(dict)['config']

    if 'id' not in config:
        config = await _get_config(config['host'], config['token'], load_tb_file=False)

    response = await client.workspaces()

    columns = ['name', 'id', 'role', 'plan', 'current']
    table = []
    click.echo(FeedbackManager.info_current_workspace())

    for workspace in response['workspaces']:
        if config['id'] == workspace['id']:
            table.append([workspace['name'], workspace['id'], workspace['role'], _get_workspace_plan_name(workspace['plan']), True])

    click.echo(humanfriendly.tables.format_smart_table(table, column_names=columns))

    if yes or click.confirm(FeedbackManager.warning_confirm_clear_workspace()):

        pipes = await client.pipes(dependencies=False, node_attrs='name', attrs='name')
        pipe_names = [pipe['name'] for pipe in pipes]
        for pipe_name in pipe_names:
            if not dry_run:
                click.echo(FeedbackManager.info_removing_pipe(pipe=pipe_name))
                try:
                    await client.pipe_delete(pipe_name)
                except DoesNotExistException:
                    click.echo(FeedbackManager.info_removing_pipe_not_found(pipe=pipe_name))
            else:
                click.echo(FeedbackManager.info_dry_removing_pipe(pipe=pipe_name))

        datasources = await client.datasources()
        ds_names = [datasource['name'] for datasource in datasources]
        for ds_name in ds_names:
            if not dry_run:
                click.echo(FeedbackManager.info_removing_datasource(datasource=ds_name))
                try:
                    await client.datasource_delete(ds_name)
                    print(ds_names, ds_name)
                except DoesNotExistException:
                    click.echo(FeedbackManager.info_removing_datasource_not_found(datasource=ds_name))
                except CanNotBeDeletedException as e:
                    click.echo(FeedbackManager.error_datasource_can_not_be_deleted(datasource=ds_name, error=e))
                except Exception as e:
                    if ("is a Shared Data Source" in str(e)):
                        click.echo(FeedbackManager.error_operation_can_not_be_performed(error=e))
                    else:
                        raise click.ClickException(FeedbackManager.error_exception(error=e))
            else:
                click.echo(FeedbackManager.info_dry_removing_datasource(datasource=ds_name))


def ask_for_user_token(action: str, ui_host: str) -> str:
    return click.prompt(f"\nIn order to {action} we need your user token. Copy it from {ui_host}/tokens and paste it here",
                        hide_input=True,
                        show_default=False,
                        default=None)


async def get_available_starterkits(ctx: Context) -> List[Dict[str, Any]]:
    ctx_dict = ctx.ensure_object(dict)
    available_starterkits = ctx_dict.get('available_starterkits', None)
    if available_starterkits is not None:
        return available_starterkits

    try:
        client: TinyB = ctx_dict['client']

        available_starterkits = await client.starterkits()
        ctx_dict['available_starterkits'] = available_starterkits
        return available_starterkits
    except Exception as ex:
        click.echo(FeedbackManager.error_exception(error=ex))
        return []


async def get_starterkit(ctx: Context, name: str) -> Optional[Dict[str, Any]]:
    available_starterkits = await get_available_starterkits(ctx)
    if not available_starterkits:
        return None
    return next((sk for sk in available_starterkits if sk.get('friendly_name', None) == name), None)


async def is_valid_starterkit(ctx: Context, name: str) -> bool:
    return await get_starterkit(ctx, name) is not None


async def ask_for_starterkit_interactively(ctx: Context) -> Optional[str]:
    starterkit = [{'friendly_name': 'blank', 'description': 'Empty workspace'}]
    starterkit.extend(await get_available_starterkits(ctx))
    rows = [(index + 1, sk['friendly_name'], sk['description']) for index, sk in enumerate(starterkit)]

    print(humanfriendly.tables.format_smart_table(rows, column_names=['Idx', 'Id', 'Description']))
    print("")
    print("   [0] to cancel")

    sk_index = -1
    while sk_index == -1:
        sk_index = click.prompt("\nUse starter kit", default=1)
        if sk_index < 0 or sk_index > len(starterkit):
            click.echo(FeedbackManager.error_starterkit_index(starterkit_index=sk_index))
            sk_index = -1

    if sk_index == 0:
        click.echo(FeedbackManager.info_cancelled_by_user())
        return None

    return starterkit[sk_index - 1]['friendly_name']


async def fork_workspace(ctx: Context, client: TinyB, user_client: TinyB, created_workspace):
    config, _, _ = await get_config_and_hosts(ctx)

    datasources = await client.datasources()
    for datasource in datasources:
        await user_client.datasource_share(datasource['id'], config['id'], created_workspace['id'])  # type: ignore


async def create_workspace_non_interactive(ctx: Context, workspace_name: str,
                                           starterkit: str, user_token: str,
                                           fork: bool):
    """Creates a workspace using the provided name and starterkit
    """
    client: TinyB = ctx.ensure_object(dict)['client']

    try:
        user_client: TinyB = deepcopy(client)
        user_client.token = user_token
        created_workspace = await user_client.create_workspace(workspace_name, starterkit)
        click.echo(FeedbackManager.success_workspace_created(workspace_name=workspace_name))

        if fork:
            await fork_workspace(ctx, client, user_client, created_workspace)

    except Exception as e:
        click.echo(FeedbackManager.error_exception(error=str(e)))


async def create_workspace_interactive(ctx: Context, workspace_name: Optional[str],
                                       starterkit: Optional[str], user_token: str,
                                       fork: bool):
    """Creates a workspace guiding the user
    """
    click.echo(FeedbackManager.info_workspace_create_greeting())

    if not starterkit:
        starterkit = await ask_for_starterkit_interactively(ctx)
        if not starterkit:  # Cancelled by user
            return

        if starterkit == 'blank':  # 'blank' == empty workspace
            starterkit = None

    if not workspace_name:
        default_name = f'new_workspace_{uuid.uuid4().hex[0:4]}'
        workspace_name = click.prompt("\nWorkspace name", default=default_name, err=True, type=str)  # type: ignore

    await create_workspace_non_interactive(ctx, workspace_name, starterkit,  # type: ignore
                                           user_token, fork)


@workspace.command(name='create', short_help="Create a new Workspace for your Tinybird user")
@click.argument('workspace_name', required=False)
@click.option('--starter-kit', type=str, required=False, help="Use a Tinybird starter kit as a template")
@click.option('--user_token', is_flag=False, default=None, help="Do not ask for your user token")
@click.option('--fork', is_flag=True, default=False, help="When enabled, we will share all datasource from the current workspace to the new created one")
@click.pass_context
@coro
async def create_workspace(ctx: Context, workspace_name: str, starter_kit: str,
                           user_token: str, fork: bool):

    if starter_kit:
        if not await is_valid_starterkit(ctx, starter_kit):
            click.echo(FeedbackManager.error_starterkit_name(starterkit_name=starter_kit))
            return

    if not user_token:
        _, _, ui_host = await get_config_and_hosts(ctx)
        user_token = ask_for_user_token('create a new workspace', ui_host)
        if not user_token:
            return

    # If we have at least workspace_name, we start the non interactive
    # process, creating an empty workspace
    if workspace_name:
        await create_workspace_non_interactive(ctx, workspace_name, starter_kit,
                                               user_token, fork)
    else:
        await create_workspace_interactive(ctx, workspace_name, starter_kit,
                                           user_token, fork)


@workspace.command(name='delete', short_help="Delete a Workspace for your Tinybird user")
@click.argument('workspace_name_or_id')
@click.option('--user_token', is_flag=False, default=False, help="Do not ask for your user token")
@click.option('--yes', is_flag=True, default=False, help="Do not ask for confirmation")
@click.pass_context
@coro
async def delete_workspace(ctx: Context, workspace_name_or_id: str, user_token: str, yes: bool):
    """Delete a workspace where you are admin"""

    client: TinyB = ctx.ensure_object(dict)['client']
    config, host, ui_host = await get_config_and_hosts(ctx)

    if not user_token:
        user_token = ask_for_user_token('delete a workspace', ui_host)

    if yes or click.confirm(FeedbackManager.warning_confirm_delete_workspace()):
        workspaces = (await client.workspaces()).get('workspaces', [])
        workspace_to_delete = next((workspace for workspace in workspaces if workspace['name'] == workspace_name_or_id or workspace['id'] == workspace_name_or_id), None)

        if not workspace_to_delete:
            raise click.ClickException(FeedbackManager.error_workspace(workspace=workspace_name_or_id))

        client.token = user_token

        try:
            await client.delete_workspace(workspace_to_delete['id'])
            click.echo(FeedbackManager.success_workspace_deleted(workspace_name=workspace_to_delete['name']))
        except Exception as e:
            click.echo(FeedbackManager.error_exception(error=str(e)))
            return


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


class PlanName(Enum):
    DEV = 'Build'
    PRO = 'Pro'
    ENTERPRISE = 'Enterprise'


def _get_workspace_plan_name(plan):
    if plan == 'dev':
        return PlanName.DEV.value
    if plan == 'pro':
        return PlanName.PRO.value
    if plan == 'enterprise':
        return PlanName.ENTERPRISE.value
    return 'Custom'


@cli.group()
@click.pass_context
def datasource(ctx):
    '''Data sources commands'''


@datasource.command(name="ls")
@click.option('--prefix', default=None, help="Show only resources with this prefix")
@click.option('--match', default=None, help='Retrieve any resources matching the pattern. eg --match _test')
@click.option('--format', 'format_', type=click.Choice(['json'], case_sensitive=False), default=None, help="Force a type of the output")
@click.pass_context
@coro
async def datasource_ls(ctx: Context, prefix: Optional[str], match: Optional[str], format_: str):
    """List data sources"""
    client: TinyB = ctx.ensure_object(dict)['client']
    ds = await client.datasources()
    columns = ['prefix', 'version', 'shared from', 'name', 'row_count', 'size', 'created at', 'updated at', 'connection']
    table_human_readable = []
    table_machine_readable = []
    pattern = re.compile(match) if match else None

    for t in ds:
        stats = t.get('stats', None)
        if not stats:
            stats = t.get('statistics', {'bytes': ''})
            if not stats:
                stats = {'bytes': ''}

        tk = get_name_tag_version(t['name'])
        if (prefix and tk['tag'] != prefix) or (pattern and not pattern.search(tk['name'])):
            continue

        if "." in tk['name']:
            shared_from, name = tk['name'].split(".")
        else:
            shared_from, name = '', tk['name']

        table_human_readable.append((
            tk['tag'] or '',
            tk['version'] if tk['version'] is not None else '',
            shared_from,
            name,
            humanfriendly.format_number(stats.get('row_count')) if stats.get('row_count', None) else '-',
            humanfriendly.format_size(int(stats.get('bytes'))) if stats.get('bytes', None) else '-',
            t['created_at'][:-7],
            t['updated_at'][:-7],
            t.get('service', '')
        ))
        table_machine_readable.append({
            'prefix': tk['tag'] or '',
            'version': tk['version'] if tk['version'] is not None else '',
            'shared from': shared_from,
            'name': name,
            'row_count': stats.get('row_count', None) or '-',
            'size': stats.get('bytes', None) or '-',
            'created at': t['created_at'][:-7],
            'updated at': t['updated_at'][:-7],
            'connection': t.get('service', '')
        })

    if not format_:
        click.echo(FeedbackManager.info_datasources())
        click.echo(humanfriendly.tables.format_smart_table(table_human_readable, column_names=columns))
        click.echo('\n')
    elif format_ == 'json':
        click.echo(json.dumps({'datasources': table_machine_readable}, indent=2))
    else:
        click.echo(FeedbackManager.error_datasource_ls_type)


def get_format_from_filename_or_url(filename_or_url: str) -> str:
    """
    >>> get_format_from_filename_or_url('wadus_parquet.csv')
    'csv'
    >>> get_format_from_filename_or_url('wadus_csv.parquet')
    'parquet'
    >>> get_format_from_filename_or_url('wadus_csv.ndjson')
    'ndjson'
    >>> get_format_from_filename_or_url('wadus_csv.json')
    'ndjson'
    >>> get_format_from_filename_or_url('wadus_parquet.csv?auth=pepe')
    'csv'
    >>> get_format_from_filename_or_url('wadus_csv.parquet?auth=pepe')
    'parquet'
    >>> get_format_from_filename_or_url('wadus_parquet.ndjson?auth=pepe')
    'ndjson'
    >>> get_format_from_filename_or_url('wadus.json?auth=pepe')
    'ndjson'
    >>> get_format_from_filename_or_url('wadus_csv_')
    'csv'
    >>> get_format_from_filename_or_url('wadus_json_csv_')
    'csv'
    >>> get_format_from_filename_or_url('wadus_json_')
    'ndjson'
    >>> get_format_from_filename_or_url('wadus_ndjson_')
    'ndjson'
    >>> get_format_from_filename_or_url('wadus_parquet_')
    'parquet'
    >>> get_format_from_filename_or_url('wadus')
    'csv'
    >>> get_format_from_filename_or_url('https://storage.googleapis.com/tinybird-waduscom/stores_stock__v2_1646741850424_final.csv?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=44444444444-compute@developer.gserviceaccount.com/1234/auto/storage/goog4_request&X-Goog-Date=20220308T121750Z&X-Goog-Expires=86400&X-Goog-SignedHeaders=host&X-Goog-Signature=8888888888888888888888888888888888888888888888888888888')
    'csv'
    """
    filename_or_url = filename_or_url.lower()
    if filename_or_url.endswith('json') or filename_or_url.endswith('ndjson'):
        return 'ndjson'
    if filename_or_url.endswith('parquet'):
        return 'parquet'
    if filename_or_url.endswith('csv'):
        return 'csv'
    try:
        parsed = urlparse(filename_or_url)
        if parsed.path.endswith('json') or parsed.path.endswith('ndjson'):
            return 'ndjson'
        if parsed.path.endswith('parquet'):
            return 'parquet'
        if parsed.path.endswith('csv'):
            return 'csv'
    except Exception:
        pass
    if 'csv' in filename_or_url:
        return 'csv'
    if 'json' in filename_or_url:
        return 'ndjson'
    if 'parquet' in filename_or_url:
        return 'parquet'
    return 'csv'


async def push_data(ctx, datasource_name, url, connector, sql, mode='append', sql_condition=None, replace_options=None, ignore_empty=False):
    if url and type(url) is tuple:
        url = url[0]
    client = ctx.obj['client']

    if connector:
        load_connector_config(ctx, connector, False, check_uninstalled=False)
        if connector not in ctx.obj:
            click.echo(FeedbackManager.error_connector_not_configured(connector=connector))
            return
        else:
            _connector = ctx.obj[connector]
            click.echo(FeedbackManager.info_starting_export_process(connector=connector))
            try:
                url = _connector.export_to_gcs(sql, datasource_name, mode)
            except ConnectorNothingToLoad as e:
                if ignore_empty:
                    click.echo(str(e))
                    return
                else:
                    raise e

    def cb(res):
        if cb.First:
            blocks_to_process = len([x for x in res['block_log'] if x['status'] == 'idle'])
            if blocks_to_process:
                cb.bar = click.progressbar(label=FeedbackManager.info_progress_blocks(), length=blocks_to_process)
                cb.bar.update(0)
                cb.First = False
                cb.blocks_to_process = blocks_to_process
        else:
            done = len([x for x in res['block_log'] if x['status'] == 'done'])
            if done * 2 > cb.blocks_to_process:
                cb.bar.label = FeedbackManager.info_progress_current_blocks()
            cb.bar.update(done - cb.prev_done)
            cb.prev_done = done
    cb.First = True
    cb.prev_done = 0

    click.echo(FeedbackManager.info_starting_import_process())

    if isinstance(url, list):
        urls = url
    else:
        urls = [url]

    try:
        for url in urls:
            parsed = urlparse(url)
            # poor man's format detection
            _format = get_format_from_filename_or_url(url)
            if parsed.scheme in ('http', 'https'):
                res = await client.datasource_create_from_url(datasource_name, url, mode=mode, status_callback=cb, sql_condition=sql_condition, format=_format, replace_options=replace_options)
            else:
                with open(url, mode='rb') as file:
                    res = await client.datasource_append_data(datasource_name, file, mode=mode, sql_condition=sql_condition, format=_format, replace_options=replace_options)

            datasource_name = res['datasource']['name']
            try:
                datasource = await client.get_datasource(datasource_name)
            except DoesNotExistException:
                click.echo(FeedbackManager.error_datasource_does_not_exist(datasource=datasource_name))
            except Exception as e:
                click.echo(FeedbackManager.error_exception(error=str(e)))
                return

            total_rows = (datasource.get('statistics', {}) or {}).get('row_count', 0)
            appended_rows = 0
            parser = None

            if 'error' in res and res['error']:
                click.echo(FeedbackManager.error_exception(error=res['error']))
            if 'errors' in res and res['errors']:
                click.echo(FeedbackManager.error_exception(error=res['errors']))
            if 'blocks' in res and res['blocks']:
                for block in res['blocks']:
                    process_return = block['process_return'][0]
                    parser = process_return['parser'] if 'parser' in process_return and process_return['parser'] else parser
                    if parser and parser != 'clickhouse':
                        parser = process_return['parser']
                        appended_rows += process_return['lines']

    except OperationCanNotBePerformed as e:
        click.echo(FeedbackManager.error_operation_can_not_be_performed(error=e))
    except Exception as e:
        click.echo(FeedbackManager.error_exception(error=e))
        sys.exit(1)
    else:
        click.echo(FeedbackManager.success_progress_blocks())
        if mode == 'append':
            if parser != 'clickhouse':
                click.echo(FeedbackManager.success_appended_rows(appended_rows=appended_rows))

        click.echo(FeedbackManager.success_total_rows(datasource=datasource_name, total_rows=total_rows))

        if mode == 'replace':
            click.echo(FeedbackManager.success_replaced_datasource(datasource=datasource_name))
        else:
            click.echo(FeedbackManager.success_appended_datasource(datasource=datasource_name))
        click.echo(FeedbackManager.info_data_pushed(datasource=datasource_name))
    finally:
        try:
            for url in urls:
                _connector.clean(urlparse(url).path.split('/')[-1])
        except Exception:
            pass


@datasource.command(name="append")
@click.argument('datasource_name')
@click.argument('url', nargs=-1)
@click.option('--connector', type=click.Choice(['bigquery', 'snowflake'], case_sensitive=True), help="Import from one of the selected connectors", hidden=True)
@click.option('--sql', default=None, help='Query to extract data from one of the SQL connectors', hidden=True)
@click.option('--incremental', default=None, help='It does an incremental append, taking the max value for the date column name provided as a parameter. It only works when the `connector` parameter is passed.', hidden=True)
@click.option('--ignore-empty', help='Wheter or not to ignore empty results from the connector', is_flag=True, default=False, hidden=True)
@click.pass_context
@coro
async def datasource_append(ctx, datasource_name, url, connector, sql, incremental, ignore_empty):
    """
        Create a data source from a URL, local file or a connector

        - Load from URL `tb datasource append [datasource_name] https://url_to_csv`

        - Load from local file `tb datasource append [datasource_name] /path/to/local/file`

        - Load from connector `tb datasource append [datasource_name] --connector [connector_name] --sql [the_sql_to_extract_from]`
    """
    if incremental and not connector:
        click.echo(FeedbackManager.error_incremental_not_supported())
        return

    if incremental:
        date = None
        source_column = incremental.split(':')[0]
        dest_column = incremental.split(':')[-1]
        result = await ctx.obj['client'].query(f'SELECT max({dest_column}) as inc from {datasource_name} FORMAT JSON')
        try:
            date = result['data'][0]['inc']
        except Exception as e:
            raise click.ClickException(f'{str(e)}')
        if date:
            sql = f"{sql} WHERE {source_column} > '{date}'"
    await push_data(ctx, datasource_name, url, connector, sql, mode='append', ignore_empty=ignore_empty)


@datasource.command(name="replace")
@click.argument('datasource_name')
@click.argument('url', nargs=-1)
@click.option('--connector', type=click.Choice(['bigquery', 'snowflake'], case_sensitive=True), help="Import from one of the selected connectors", hidden=True)
@click.option('--sql', default=None, help='Query to extract data from one of the SQL connectors', hidden=True)
@click.option('--sql-condition', default=None, help='SQL WHERE condition to replace data', hidden=True)
@click.option('--skip-incompatible-partition-key', is_flag=True, default=False, hidden=True)
@click.option('--ignore-empty', help='Wheter or not to ignore empty results from the connector', is_flag=True, default=False, hidden=True)
@click.pass_context
@coro
async def datasource_replace(ctx, datasource_name, url, connector, sql, sql_condition, skip_incompatible_partition_key, ignore_empty: bool):
    """
        Replaces the data in a data source from a URL, local file or a connector

        - Replace from URL `tb datasource replace [datasource_name] https://url_to_csv --sql-condition "country='ES'"`

        - Replace from local file `tb datasource replace [datasource_name] /path/to/local/file --sql-condition "country='ES'"`

        - Replace from connector `tb datasource replace [datasource_name] --connector [connector_name] --sql [the_sql_to_extract_from] --sql-condition "country='ES'"`
    """
    replace_options = set()
    if skip_incompatible_partition_key:
        replace_options.add("skip_incompatible_partition_key")
    await push_data(ctx, datasource_name, url, connector, sql, mode='replace', sql_condition=sql_condition, replace_options=replace_options, ignore_empty=ignore_empty)


@datasource.command(name='analyze')
@click.argument('url_or_file')
@click.option('--connector', type=click.Choice(['bigquery', 'snowflake'], case_sensitive=True), help="Use from one of the selected connectors. In this case pass a table name as a parameter instead of a file name or an URL", hidden=True)
@click.pass_context
@coro
async def datasource_analyze(ctx, url_or_file, connector):
    '''Analyze a URL or a file before creating a new data source'''
    client = ctx.obj['client']

    _connector = None
    if connector:
        load_connector_config(ctx, connector, False, check_uninstalled=False)
        if connector not in ctx.obj:
            click.echo(FeedbackManager.error_connector_not_configured(connector=connector))
            return
        else:
            _connector = ctx.obj[connector]

    def _table(title, columns, data):
        row_format = "{:<25}" * len(columns)
        click.echo(FeedbackManager.info_datasource_title(title=title))
        click.echo(FeedbackManager.info_datasource_row(row=row_format.format(*columns)))
        for t in data:
            click.echo(FeedbackManager.info_datasource_row(row=row_format.format(*[str(element) for element in t])))

    analysis, _ = await _analyze(url_or_file, client, format=get_format_from_filename_or_url(url_or_file), connector=_connector)

    columns = ('name', 'type', 'nullable')
    if 'columns' in analysis['analysis']:
        _table('columns', columns, [(t['name'], t['recommended_type'], 'false' if t['present_pct'] == 1 else 'true') for t in analysis['analysis']['columns']])

    click.echo(FeedbackManager.info_datasource_title(title='SQL Schema'))
    click.echo(analysis['analysis']['schema'])

    values = []

    if 'dialect' in analysis:
        for x in analysis['dialect'].items():
            if x[1] == ' ':
                values.append((x[0], '" "'))
            elif type(x[1]) == str and ('\n' in x[1] or '\r' in x[1]):
                values.append((x[0], x[1].replace('\n', '\\n'). replace('\r', '\\r')))
            else:
                values.append(x)

        _table('dialect', ('name', 'value'), values)


@datasource.command(name="rm")
@click.argument('datasource_name')
@click.option('--yes', is_flag=True, default=False, help="Do not ask for confirmation")
@click.pass_context
@coro
async def datasource_delete(ctx: Context, datasource_name: str, yes: bool):
    """Delete a data source"""
    client: TinyB = ctx.ensure_object(dict)['client']
    try:
        datasource = await client.get_datasource(datasource_name)
    except DoesNotExistException:
        raise click.ClickException(FeedbackManager.error_datasource_does_not_exist(datasource=datasource_name))
    except Exception as e:
        raise click.ClickException(FeedbackManager.error_exception(error=e))
    connector = datasource.get('service', False)

    if connector:
        click.echo(FeedbackManager.warning_datasource_is_connected(datasource=datasource_name, connector=connector))

    if yes or click.confirm(FeedbackManager.warning_confirm_delete_datasource(datasource=datasource_name)):
        try:
            await client.datasource_delete(datasource_name)
        except DoesNotExistException:
            raise click.ClickException(FeedbackManager.error_datasource_does_not_exist(datasource=datasource_name))
        except CanNotBeDeletedException as e:
            raise click.ClickException(FeedbackManager.error_datasource_can_not_be_deleted(datasource=datasource_name, error=e))
        except Exception as e:
            raise click.ClickException(FeedbackManager.error_exception(error=e))

        click.echo(FeedbackManager.success_delete_datasource(datasource=datasource_name))


@datasource.command(name="truncate")
@click.argument('datasource_name', required=True)
@click.option('--yes', is_flag=True, default=False, help="Do not ask for confirmation")
@click.option('--cascade', is_flag=True, default=False, help="Truncate dependent DS attached in cascade to the given DS")
@click.pass_context
@coro
async def datasource_truncate(ctx, datasource_name, yes, cascade):
    """Truncate a data source"""

    client = ctx.obj['client']
    if yes or click.confirm(FeedbackManager.warning_confirm_truncate_datasource(datasource=datasource_name)):
        try:
            await client.datasource_truncate(datasource_name)
        except DoesNotExistException:
            raise click.ClickException(FeedbackManager.error_datasource_does_not_exist(datasource=datasource_name))
        except Exception as e:
            raise click.ClickException(FeedbackManager.error_exception(error=e))

        click.echo(FeedbackManager.success_truncate_datasource(datasource=datasource_name))

        if (cascade):
            try:
                ds_cascade_dependencies = await client.datasource_dependencies(no_deps=False, match=None, pipe=None, datasource=datasource_name, check_for_partial_replace=True, recursive=False)
            except Exception as e:
                raise click.ClickException(FeedbackManager.error_exception(error=e))

            cascade_dependent_ds = list(ds_cascade_dependencies.get('dependencies', {}).keys()) + list(ds_cascade_dependencies.get('incompatible_datasources', {}).keys())
            for cascade_ds in cascade_dependent_ds:
                if yes or click.confirm(FeedbackManager.warning_confirm_truncate_datasource(datasource=cascade_ds)):
                    try:
                        await client.datasource_truncate(cascade_ds)
                    except DoesNotExistException:
                        click.echo(FeedbackManager.error_datasource_does_not_exist(datasource=datasource_name))
                    except Exception as e:
                        click.echo(FeedbackManager.error_exception(error=e))
                    click.echo(FeedbackManager.success_truncate_datasource(datasource=cascade_ds))


@datasource.command(name="delete")
@click.argument('datasource_name')
@click.option('--sql-condition', default=None, help='SQL WHERE condition to remove rows', hidden=True, required=True)
@click.option('--yes', is_flag=True, default=False, help="Do not ask for confirmation")
@click.option('--wait', is_flag=True, default=False, help="Wait for delete job to finish, disabled by default")
@click.pass_context
@coro
async def datasource_delete_rows(ctx, datasource_name, sql_condition, yes, wait):
    """
    Delete rows from a datasource

    - Delete rows with SQL condition: `tb datasource delete [datasource_name] --sql-condition "country='ES'"`

    - Delete rows with SQL condition and wait for the job to finish: `tb datasource delete [datasource_name] --sql-condition "country='ES'" --wait`
    """
    client: TinyB = ctx.ensure_object(dict)['client']
    if yes or click.confirm(FeedbackManager.warning_confirm_delete_rows_datasource(datasource=datasource_name, delete_condition=sql_condition)):
        try:
            res = await client.datasource_delete_rows(datasource_name, sql_condition)
            job_id = res['job_id']
            job_url = res['job_url']
            click.echo(FeedbackManager.info_datasource_delete_rows_job_url(url=job_url))
            if wait:
                progress_symbols = ['-', '\\', '|', '/']
                progress_str = 'Waiting for the job to finish'
                print(f'\n{progress_str}', end="")

                def progress_line(n):
                    print(f'\r{progress_str} {progress_symbols[n % len(progress_symbols)]}', end="")
                i = 0
                while True:
                    try:
                        res = await client._req(f'v0/jobs/{job_id}')
                    except Exception:
                        click.echo(FeedbackManager.error_job_status(url=job_url))
                        break
                    if res['status'] == 'done':
                        print('\n')
                        click.echo(FeedbackManager.success_delete_rows_datasource(datasource=datasource_name, delete_condition=sql_condition))
                        break
                    elif res['status'] == 'error':
                        print('\n')
                        click.echo(FeedbackManager.error_exception(error=res['error']))
                        break
                    await asyncio.sleep(1)
                    i += 1
                    progress_line(i)

        except DoesNotExistException:
            raise click.ClickException(FeedbackManager.error_datasource_does_not_exist(datasource=datasource_name))
        except Exception as e:
            raise click.ClickException(FeedbackManager.error_exception(error=e))


@datasource.command(name="generate", short_help="Generates a data source file based on a sample CSV, NDJSON or Parquet file from local disk or url")
@click.argument('filenames', nargs=-1, default=None)
@click.option('--force', is_flag=True, default=False, help="Override existing files")
@click.option('--connector', type=click.Choice(['bigquery', 'snowflake'], case_sensitive=True), help="Use from one of the selected connectors. In this case pass a table name as a parameter instead of a file name", hidden=True)
@click.pass_context
@coro
async def generate_datasource(ctx: Context, connector: str, filenames, force: bool):
    """Generate a data source file based on a sample CSV file from local disk or url"""
    client: TinyB = ctx.ensure_object(dict)['client']

    _connector: Optional[Connector] = None
    if connector:
        load_connector_config(ctx, connector, False, check_uninstalled=False)
        if connector not in ctx.ensure_object(dict):
            click.echo(FeedbackManager.error_connector_not_configured(connector=connector))
            return
        else:
            _connector = ctx.ensure_object(dict)[connector]

    for filename in filenames:
        await _generate_datafile(filename, client, force=force, format=get_format_from_filename_or_url(filename), connector=_connector)


# eval "$(_TB_COMPLETE=source_bash tb)"
def autocomplete_topics(ctx: Context, args, incomplete):
    try:
        config = async_to_sync(get_config)(None, None)
        ctx.ensure_object(dict)['config'] = config
        client = create_tb_client(ctx)
        topics = async_to_sync(client.kafka_list_topics)(args[2])
        return [t for t in topics if incomplete in t]
    except Exception:
        return []


@datasource.command(name="connect")
@click.argument('connection_id')
@click.argument('datasource_name')
@click.option('--topic', help="Kafka topic", autocompletion=autocomplete_topics)
@click.option('--group', help="Kafka group ID")
@click.option('--auto-offset-reset', default=None, help='Kafka auto.offset.reset config. Valid values are: ["latest", "earliest"]')
@click.pass_context
@coro
# Example usage: tb datasource connect 776824da-ac64-4de4-b8b8-b909f69d5ed5 new_ds --topic a --group b --auto-offset-reset latest
async def datasource_connect(ctx, connection_id, datasource_name, topic, group, auto_offset_reset):
    """Create a new datasource from an existing connection"""
    validate_connection_id(connection_id)
    validate_datasource_name(datasource_name)
    topic and validate_kafka_topic(topic)
    group and validate_kafka_group(group)
    auto_offset_reset and validate_kafka_auto_offset_reset(auto_offset_reset)
    client = ctx.obj['client']
    # TODO check connection id is valid
    if not topic:
        try:
            topics = await client.kafka_list_topics(connection_id)
            click.echo("We've discovered the following topics:")
            for t in topics:
                click.echo(f"    {t}")
        except Exception as e:
            logging.debug(f"Error listing topics: {e}")
        topic = click.prompt("Kafka topic")
        validate_kafka_topic(topic)
    if not group:
        group = click.prompt("Kafka group")
        validate_kafka_group(group)
    if not auto_offset_reset:
        # TODO commits? with preview
        if False:
            auto_offset_reset = "earliest"
            click.echo("Prior commits have been detected on this topic and group ID.")
            click.echo("By continuing we'll read from and commit to this group.")
        else:
            click.echo("Kafka doesn't seem to have prior commits on this topic and group ID")
            click.echo("Setting auto.offset.reset is required. Valid values:")
            click.echo("  latest          Skip earlier messages and ingest only new messages")
            click.echo("  earliest        Start ingestion from the first message")
            auto_offset_reset = click.prompt("Kafka auto.offset.reset config")
            validate_kafka_auto_offset_reset(auto_offset_reset)
        if not click.confirm("Proceed?"):
            return
    resp = await client.datasource_kafka_connect(connection_id, datasource_name, topic, group, auto_offset_reset)
    datasource_id = resp['datasource']['id']
    click.echo(FeedbackManager.success_datasource_kafka_connected(id=datasource_id))


def validate_datasource_name(name):
    if not isinstance(name, str) or str == "":
        raise click.ClickException(FeedbackManager.error_datasource_name())


def validate_connection_id(connection_id):
    if not isinstance(connection_id, str) or str == "":
        raise click.ClickException(FeedbackManager.error_datasource_connection_id())


def validate_kafka_topic(topic):
    if not isinstance(topic, str):
        raise click.ClickException(FeedbackManager.error_kafka_topic())


def validate_kafka_group(group):
    if not isinstance(group, str):
        raise click.ClickException(FeedbackManager.error_kafka_group())


def validate_kafka_auto_offset_reset(auto_offset_reset):
    valid_values = {"latest", "earliest", "none"}
    if not (auto_offset_reset in valid_values):
        raise click.ClickException(FeedbackManager.error_kafka_auto_offset_reset())


@datasource.command(name="share")
@click.argument('datasource_name')
@click.argument('workspace_name_or_id')
@click.option('--user_token', default=None, help="When passed, we won't prompt asking for it")
@click.option('--yes', is_flag=True, default=False, help="Do not ask for confirmation")
@click.pass_context
@coro
async def datasource_share(ctx: Context, datasource_name: str, workspace_name_or_id: str, user_token: str, yes: bool):
    """Share a datasource"""

    client: TinyB = ctx.ensure_object(dict)['client']

    config, host, ui_host = await get_config_and_hosts(ctx)

    datasource: Dict[str, Any] = await client.get_datasource(datasource_name)
    workspaces: List[Dict[str, Any]] = (await client.workspaces()).get('workspaces', [])
    destination_workspace = next((workspace for workspace in workspaces if workspace['name'] == workspace_name_or_id or workspace['id'] == workspace_name_or_id), None)
    current_workspace = next((workspace for workspace in workspaces if workspace['id'] == config['id']), None)  # type: ignore

    if not destination_workspace:
        click.echo(FeedbackManager.error_workspace(workspace=workspace_name_or_id))
        return

    if not current_workspace:
        click.echo(FeedbackManager.error_not_authenticated())
        return

    if not user_token:
        user_token = click.prompt(
            f"\nIn order to create a new workspace we need your user token. Copy it from {ui_host}/tokens and paste it here",
            hide_input=True)

    client.token = user_token

    if yes or click.confirm(
        FeedbackManager.warning_datasource_share(datasource=datasource_name, source_workspace=current_workspace.get('name'), destination_workspace=destination_workspace['name'])
    ):
        try:
            await client.datasource_share(
                datasource_id=datasource.get('id', ''),
                current_workspace_id=current_workspace.get('id', ''),
                destination_workspace_id=destination_workspace.get('id', ''))
            click.echo(FeedbackManager.success_datasource_shared(datasource=datasource_name, workspace=destination_workspace['name']))
        except Exception as e:
            click.echo(FeedbackManager.error_exception(error=str(e)))
            return


@cli.command()
@click.argument('query')
@click.option('--rows_limit', default=100, help="Max number of rows retrieved")
@click.option('--format', 'format_', type=click.Choice(['json', 'csv', 'human'], case_sensitive=False), default='human', help="Output format")
@click.option('--stats/--no-stats', default=False, help="Show query stats")
@click.pass_context
@coro
async def sql(ctx, query, rows_limit, format_, stats):
    """Run SQL query over data sources and pipes"""
    client = ctx.obj['client']
    q = query.lower().strip()
    if q.startswith('insert'):
        click.echo(FeedbackManager.error_invalid_query())
        click.echo(FeedbackManager.info_append_data())
        return
    if q.startswith('delete'):
        click.echo(FeedbackManager.error_invalid_query())
        return

    req_format = 'CSVWithNames' if format_ == 'csv' else 'JSON'
    try:
        res = await client.query(f'SELECT * FROM ({query}) LIMIT {rows_limit} FORMAT {req_format}')
    except Exception as e:
        click.echo(FeedbackManager.error_exception(error=str(e)))
        return
    req_format = 'CSVWithNames' if format_ == 'csv' else 'JSON'
    parsed_query = f'SELECT * FROM ({query}) LIMIT {rows_limit} FORMAT {req_format}'
    res = await client.query(parsed_query)

    if 'error' in res:
        click.echo(FeedbackManager.error_exception(error=res['error']))
        return

    if stats:
        stats_query = f'SELECT * FROM ({query}) LIMIT {rows_limit} FORMAT JSON'
        stats_res = await client.query(stats_query)
        stats = stats_res['statistics']
        seconds = stats['elapsed']
        rows_read = humanfriendly.format_number(stats['rows_read'])
        bytes_read = humanfriendly.format_size(stats['bytes_read'])
        click.echo(FeedbackManager.info_query_stats(seconds=seconds, rows=rows_read, bytes=bytes_read))

    if format_ == 'csv':
        print(res)
    elif 'data' in res and res['data']:
        if format_ == 'json':
            print(json.dumps(res, indent=8))
        else:
            dd = []
            for d in res['data']:
                dd.append(d.values())
            click.echo(humanfriendly.tables.format_smart_table(dd, column_names=res['data'][0].keys()))
    else:
        click.echo(FeedbackManager.info_no_rows())


@cli.group()
@click.pass_context
def pipe(ctx):
    '''Pipes commands'''


@pipe.command(name="generate", short_help="Generates a pipe file based on a sql query")
@click.argument('name')
@click.argument('query')
@click.option('--force', is_flag=True, default=False, help="Override existing files")
@click.pass_context
def generate_pipe(ctx, name, query, force):
    pipefile = f"""
NODE endpoint
DESCRIPTION >
    Generated from the command line
SQL >
    {query}

    """
    base = Path('endpoints')
    if not base.exists():
        base = Path()
    f = base / (f"{name}.pipe")
    if not f.exists() or force:
        with open(f'{f}', 'w') as file:
            file.write(pipefile)
        click.echo(FeedbackManager.success_generated_pipe(file=f))
    else:
        click.echo(FeedbackManager.error_exception(error=f'File {f} already exists, use --force to override'))


@cli.command(name="materialize", short_help="Given a local Pipe datafile (.pipe) and a node name it generates the target Data Source and materialized Pipe ready to be pushed and guides you through the process to create the materialized view")
@click.argument('filename', type=click.Path(exists=True))
@click.argument('target_datasource', default=None, required=False)
@click.option('--prefix', default='', help="Use prefix for all the resources")
@click.option('--push-deps', is_flag=True, default=False, help="Push dependencies, disabled by default")
@click.option('--workspace_map', nargs=2, type=str, multiple=True, hidden=True)
@click.option('--workspace', nargs=2, type=str, multiple=True, help="add a workspace path to the list of external workspaces, usage: --workspace name path/to/folder")
@click.option('--no-versions', is_flag=True, default=False, help="when set, resource dependency versions are not used, it pushes the dependencies as-is")
@click.option('--verbose', is_flag=True, default=False, help="Prints more log")
@click.option('--force-populate', default=False, required=False, help="subset or full", hidden=True)
@click.option('--override-pipe', is_flag=True, default=False, help="Override pipe if exists or prompt", hidden=True)
@click.option('--override-datasource', is_flag=True, default=False, help="Override data source if exists or prompt", hidden=True)
@click.pass_context
@coro
async def materialize(ctx, filename, prefix, push_deps, workspace_map, workspace, no_versions, verbose, force_populate, override_pipe, override_datasource, target_datasource=None):
    """[BETA] Given a local Pipe datafile path (FILENAME) and optionally a Materialized View name (TARGET_DATASOURCE), choose one of its nodes to materialize.

    This command guides you to generate the Materialized View with name TARGET_DATASOURCE, the only requirement is having a valid Pipe datafile locally. Use `tb pull` to download resources from your workspace when needed.

    Syntax: tb materialize path/to/pipe.pipe
    """
    cl = create_tb_client(ctx)

    async def _try_push_pipe_to_analyze(pipe_name):
        try:
            to_run = await folder_push(
                cl,
                tag=prefix,
                filenames=[filename],
                dry_run=False,
                check=False,
                push_deps=push_deps,
                debug=False,
                force=False,
                workspace_map=dict(workspace_map),
                workspace_lib_paths=workspace,
                no_versions=no_versions,
                run_tests=False,
                as_standard=True,
                raise_on_exists=True,
                verbose=verbose
            )
        except AlreadyExistsException as e:
            if 'Datasource' in str(e):
                click.echo(str(e))
                return
            if override_pipe or click.confirm(FeedbackManager.info_pipe_exists(name=pipe_name)):
                to_run = await folder_push(
                    cl,
                    tag=prefix,
                    filenames=[filename],
                    dry_run=False,
                    check=False,
                    push_deps=push_deps,
                    debug=False,
                    force=True,
                    workspace_map=dict(workspace_map),
                    workspace_lib_paths=workspace,
                    no_versions=no_versions,
                    run_tests=False,
                    as_standard=True,
                    verbose=verbose
                )
            else:
                return
        except click.ClickException as e:
            click.echo(str(e))

        return to_run

    def _choose_node_name(pipe):
        node = pipe['nodes'][0]
        materialized_nodes = [node for node in pipe['nodes'] if node['type'].lower() == 'materialized']

        if len(materialized_nodes) == 1:
            node = materialized_nodes[0]

        if len(pipe['nodes']) > 1 and len(materialized_nodes) != 1:
            for index, node in enumerate(pipe['nodes'], start=1):
                click.echo(f"  [{index}] Materialize node with name => {node['name']}")
            option = click.prompt(FeedbackManager.prompt_choose_node(), default=len(pipe['nodes']))
            node = pipe['nodes'][option - 1]
        node_name = node['name']
        return node, node_name

    def _choose_target_datasource_name(pipe, node, node_name):
        datasource_name = target_datasource or node.get('datasource', None) or f'mv_{pipe["resource_name"]}_{node_name}'
        if prefix:
            datasource_name = ''.join(datasource_name.split(f'{prefix}__')[1:])
        return datasource_name

    def _save_local_backup_pipe(pipe):
        pipe_bak = f'{filename}_bak'
        shutil.copyfile(filename, pipe_bak)
        pipe_file_name = f"{pipe['resource_name']}.pipe"
        if prefix:
            pipe_file_name = ''.join(pipe_file_name.split(f'{prefix}__')[1:])

        click.echo(FeedbackManager.info_pipe_backup_created(name=pipe_bak))
        return pipe_file_name

    def _save_local_datasource(datasource_name, ds_datafile):
        base = Path('datasources')
        if not base.exists():
            base = Path()
        file_name = f"{datasource_name}.datasource"
        f = base / file_name
        with open(f'{f}', 'w') as file:
            file.write(ds_datafile)

        click.echo(FeedbackManager.success_generated_local_file(file=f))
        return f

    async def _try_push_datasource(datasource_name, f):
        exists = False
        try:
            exists = await cl.get_datasource(datasource_name)
        except Exception:
            pass

        if exists:
            click.echo(FeedbackManager.info_materialize_push_datasource_exists(name=f.name))
            if override_datasource or click.confirm(FeedbackManager.info_materialize_push_datasource_override(name=f)):
                try:
                    await cl.datasource_delete(datasource_name)
                except DoesNotExistException:
                    pass

        filename = str(f.absolute())
        to_run = await folder_push(
            cl,
            tag=prefix,
            filenames=[filename],
            push_deps=push_deps,
            workspace_map=dict(workspace_map),
            workspace_lib_paths=workspace,
            no_versions=no_versions,
            verbose=verbose
        )
        return to_run

    def _save_local_pipe(pipe_file_name, pipe_datafile, pipe):
        base = Path('pipes')
        if not base.exists():
            base = Path()
        f_pipe = base / pipe_file_name

        with open(f'{f_pipe}', 'w') as file:
            if pipe['version'] is not None and pipe['version'] >= 0:
                pipe_datafile = f"VERSION {pipe['version']} \n {pipe_datafile}"
            prefix_name = ''
            if prefix:
                prefix_name = prefix
            matches = re.findall(rf'(({prefix_name}__)?([^\s\.]*)__v\d+)', pipe_datafile)
            for match in set(matches):
                if match[2] in pipe_datafile:
                    pipe_datafile = pipe_datafile.replace(match[0], match[2])
            file.write(pipe_datafile)

        click.echo(FeedbackManager.success_generated_local_file(file=f_pipe))
        return f_pipe

    async def _try_push_pipe(f_pipe):
        if override_pipe:
            option = 2
        else:
            click.echo(FeedbackManager.info_materialize_push_pipe_skip(name=f_pipe.name))
            click.echo(FeedbackManager.info_materialize_push_pipe_override(name=f_pipe.name))
            option = click.prompt(FeedbackManager.prompt_choose(), default=1)
        force = True
        check = True if option == 1 else False

        filename = str(f_pipe.absolute())
        to_run = await folder_push(
            cl,
            tag=prefix,
            filenames=[filename],
            dry_run=False,
            check=check,
            push_deps=push_deps,
            debug=False,
            force=force,
            workspace_map=dict(workspace_map),
            workspace_lib_paths=workspace,
            no_versions=no_versions,
            run_tests=False,
            verbose=verbose
        )
        return to_run

    async def _populate(pipe, node_name, f_pipe):
        if force_populate or click.confirm(FeedbackManager.prompt_populate(file=f_pipe)):
            if not force_populate:
                click.echo(FeedbackManager.info_materialize_populate_partial())
                click.echo(FeedbackManager.info_materialize_populate_full())
                option = click.prompt(FeedbackManager.prompt_choose(), default=1)
            else:
                option = 1 if force_populate == 'subset' else 2
            populate = False
            populate_subset = False
            if option == 1:
                populate_subset = 0.1
                populate = True
            elif option == 2:
                populate = True

            if populate:
                response = await cl.populate_node(pipe['name'], node_name, populate_subset=populate_subset)
                if 'job' not in response:
                    raise click.ClickException(response)

                job_id = response['job']['id']
                wait_populate = True
                if wait_populate:
                    with click.progressbar(label="Populating ", length=100, show_eta=False, show_percent=True, fill_char=click.style("█", fg="green")) as progress_bar:
                        def progressbar_cb(res):
                            if 'progress_percentage' in res:
                                progress_bar.update(int(round(res['progress_percentage'])) - progress_bar.pos)
                            elif res['status'] != 'working':
                                progress_bar.update(progress_bar.length)
                        try:
                            result = await asyncio.wait_for(cl.wait_for_job(job_id, status_callback=progressbar_cb), None)
                            if result['status'] != 'done':
                                click.echo(FeedbackManager.error_while_populating(error=result['error']))
                            else:
                                progress_bar.update(progress_bar.length)
                        except asyncio.TimeoutError:
                            await cl.job_cancel(job_id)
                            raise click.ClickException(FeedbackManager.error_while_populating(error="Reach timeout, job cancelled"))
                        except Exception as e:
                            raise click.ClickException(FeedbackManager.error_while_populating(error=str(e)))

    click.echo(FeedbackManager.warning_beta_tester())
    pipe_name = os.path.basename(filename).rsplit('.', 1)[0]
    if prefix:
        pipe_name = f'{prefix}__{pipe_name}'
    click.echo(FeedbackManager.info_before_push_materialize(name=filename))
    try:
        # extracted the materialize logic to local functions so the workflow is more readable
        to_run = await _try_push_pipe_to_analyze(pipe_name)

        if to_run is None:
            return

        pipe = to_run[pipe_name.split('/')[-1]]
        node, node_name = _choose_node_name(pipe)
        datasource_name = _choose_target_datasource_name(pipe, node, node_name)

        click.echo(FeedbackManager.info_before_materialize(name=pipe['name']))
        analysis = await cl.analyze_pipe_node(pipe['name'], node, datasource_name=datasource_name)
        ds_datafile = analysis['analysis']['datasource']['datafile']
        pipe_datafile = analysis['analysis']['pipe']['datafile']

        pipe_file_name = _save_local_backup_pipe(pipe)
        f = _save_local_datasource(datasource_name, ds_datafile)
        await _try_push_datasource(datasource_name, f)

        f_pipe = _save_local_pipe(pipe_file_name, pipe_datafile, pipe)
        await _try_push_pipe(f_pipe)
        await _populate(pipe, node_name, f_pipe)

        prefix_name = f'{prefix}__' if prefix else ''
        click.echo(FeedbackManager.success_created_matview(name=f'{prefix_name}{datasource_name}'))
    except Exception as e:
        click.echo(FeedbackManager.error_exception(error=str(e)))


@pipe.command(name="stats")
@click.argument('pipe', nargs=-1)
@click.pass_context
@coro
async def pipe_stats(ctx, pipe):
    """Print pipe stats"""
    client = ctx.obj['client']
    pipes = await client.pipes()
    pipes_to_get_stats = []
    pipes_ids = {}
    for pipe in pipes:
        name_tag = get_name_tag_version(pipe['name'])
        if name_tag['name'] in pipe['name']:
            pipes_to_get_stats.append(f"'{pipe['id']}'")
            pipes_ids[pipe['id']] = name_tag

    if not pipes_to_get_stats:
        click.echo(FeedbackManager.info_no_pipes_stats())
        return

    sql = f"""
        SELECT
            pipe_id id,
            sumIf(view_count, date > now() - interval 7 day) requests,
            sumIf(view_count, date > now() - interval 14 day and date < now() - interval 7 day) prev_requests,
            sumIf(error_count, date > now() - interval 7 day) errors,
            sumIf(error_count, date > now() - interval 14 day and date < now() - interval 7 day) prev_errors,
            avgMergeIf(avg_duration_state, date > now() - interval 7 day) latency,
            avgMergeIf(avg_duration_state, date > now() - interval 14 day and date < now() - interval 7 day) prev_latency
        FROM tinybird.pipe_stats
        where pipe_id in ({','.join(pipes_to_get_stats)})
        GROUP BY pipe_id
        ORDER BY requests DESC
        FORMAT JSON
    """

    columns = ['prefix', 'version', 'name', 'request count', 'error count', 'avg latency']
    res = await client.query(sql)
    table = []

    if res and 'error' in res:
        click.echo(FeedbackManager.error_exception(error=str(res['error'])))
        return

    if res and 'data' in res:
        for x in res['data']:
            tk = pipes_ids[x['id']]
            table.append((
                tk['tag'] or '',
                tk['version'] if tk['version'] is not None else '',
                tk['name'],
                x['requests'],
                x['errors'],
                x['latency']
            ))

        table.sort(key=lambda x: (x[2], x[1]))
        click.echo(humanfriendly.tables.format_smart_table(table, column_names=columns))


@pipe.command(name="ls")
@click.option('--prefix', default=None, help="Show only resources with this prefix")
@click.option('--match', default=None, help='Retrieve any resourcing matching the pattern. eg --match _test')
@click.option('--format', 'format_', type=click.Choice(['json'], case_sensitive=False), default=None, help="Force a type of the output")
@click.pass_context
@coro
async def pipe_ls(ctx: Context, prefix: str, match: str, format_):
    """List pipes"""

    client: TinyB = ctx.ensure_object(dict)['client']
    pipes = await client.pipes(dependencies=False, node_attrs='name', attrs='name,updated_at')
    pipes = sorted(pipes, key=lambda p: p['updated_at'])

    columns = ['prefix', 'version', 'name', 'published date', 'nodes']
    table_human_readable = []
    table_machine_readable = []
    pattern = re.compile(match) if match else None
    for t in pipes:
        tk = get_name_tag_version(t['name'])
        if (prefix and tk['tag'] != prefix) or (pattern and not pattern.search(tk['name'])):
            continue
        table_human_readable.append((
            tk['tag'] or '',
            tk['version'] if tk['version'] is not None else '',
            tk['name'],
            t['updated_at'][:-7],
            len(t['nodes'])
        ))
        table_machine_readable.append({
            'prefix': tk['tag'] or '',
            'version': tk['version'] if tk['version'] is not None else '',
            'name': tk['name'],
            'published date': t['updated_at'][:-7],
            'nodes': len(t['nodes'])
        })

    if not format_:
        click.echo(FeedbackManager.info_pipes())
        click.echo(humanfriendly.tables.format_smart_table(table_human_readable, column_names=columns))
        click.echo('\n')
    elif format_ == 'json':
        click.echo(json.dumps({'pipes': table_machine_readable}, indent=2))
    else:
        click.echo(FeedbackManager.error_pipe_ls_type)


@pipe.command(name="populate")
@click.argument('pipe_name')
@click.option('--node', type=str, help="Name of the materialized node")
@click.option('--sql-condition', type=str, default=None, help="Populate with a SQL condition to be applied to the trigger Data Source of the Materialized View. For instance, `--sql-condition='date == toYYYYMM(now())'` it'll populate taking all the rows from the trigger Data Source which `date` is the current month. Use it together with --populate. --sql-condition is not taken into account if the --subset param is present. Including in the ``sql_condition`` any column present in the Data Source ``engine_sorting_key`` will make the populate job process less data.")
@click.option('--truncate', is_flag=True, default=False, help="Truncates the materialized Data Source before populating it")
@click.option('--wait', is_flag=True, default=False, help="To be used along with --populate command. Waits for populate jobs to finish, showing a progress bar. Combined with --debug, displays the estimated remaining job times.")
@click.pass_context
@coro
async def pipe_populate(ctx, pipe_name, node, sql_condition, truncate, wait):
    cl = create_tb_client(ctx)
    response = await cl.populate_node(pipe_name, node, populate_condition=sql_condition, truncate=truncate)
    if 'job' not in response:
        raise click.ClickException(response)

    job_id = response['job']['id']
    job_url = response['job']['job_url']
    if sql_condition:
        click.echo(FeedbackManager.info_populate_condition_job_url(url=job_url, populate_condition=sql_condition))
    else:
        click.echo(FeedbackManager.info_populate_job_url(url=job_url))
    if wait:
        with click.progressbar(label="Populating ", length=100, show_eta=False, show_percent=True, fill_char=click.style("█", fg="green")) as progress_bar:
            def progressbar_cb(res):
                if 'progress_percentage' in res:
                    progress_bar.update(int(round(res['progress_percentage'])) - progress_bar.pos)
                elif res['status'] != 'working':
                    progress_bar.update(progress_bar.length)
            try:
                result = await asyncio.wait_for(cl.wait_for_job(job_id, status_callback=progressbar_cb), None)
                if result['status'] != 'done':
                    click.echo(FeedbackManager.error_while_populating(error=result['error']))
                else:
                    progress_bar.update(progress_bar.length)
            except asyncio.TimeoutError:
                await cl.job_cancel(job_id)
                raise click.ClickException(FeedbackManager.error_while_populating(error="Reach timeout, job cancelled"))
            except Exception as e:
                raise click.ClickException(FeedbackManager.error_while_populating(error=str(e)))


@pipe.command(name="new")
@click.argument('pipe_name')
@click.argument('sql')
@click.pass_context
@coro
async def pipe_create(ctx, pipe_name, sql):
    """Create a new pipe"""
    client = ctx.obj['client']
    host = ctx.obj['config'].get('host', DEFAULT_API_HOST)
    res = await client.pipe_create(pipe_name, sql)
    click.echo(FeedbackManager.success_created_pipe(pipe=pipe_name, node_id=res['nodes'][0]['id'], host=host))


@pipe.command(name="append")
@click.argument('pipe_name_or_uid')
@click.argument('sql')
@click.pass_context
@coro
async def pipe_append_node(ctx, pipe_name_or_uid, sql):
    """Append a node to a pipe"""
    client = ctx.obj['client']
    res = await client.pipe_append_node(pipe_name_or_uid, sql)
    click.echo(FeedbackManager.success_node_changed(node_id=res['id']))


async def common_pipe_publish_node(ctx, pipe_name_or_id, node_uid=None):
    """Change the published node of a pipe"""
    client = ctx.obj['client']
    host = ctx.obj['config'].get('host', DEFAULT_API_HOST)

    try:
        pipe = await client.pipe(pipe_name_or_id)
        if not node_uid:
            node = pipe['nodes'][-1]['name']
            click.echo(FeedbackManager.info_using_node(node=node))
        else:
            node = node_uid

        await client.pipe_set_endpoint(pipe_name_or_id, node)
        click.echo(FeedbackManager.success_node_published(pipe=pipe_name_or_id, host=host))
    except DoesNotExistException:
        raise click.ClickException(FeedbackManager.error_pipe_does_not_exist(pipe=pipe_name_or_id))
    except Exception as e:
        raise click.ClickException(FeedbackManager.error_exception(error=e))


@pipe.command(name="publish")
@click.argument('pipe_name_or_id')
@click.argument('node_uid', default=None, required=False)
@click.pass_context
@coro
async def pipe_publish_node(ctx, pipe_name_or_id, node_uid=None):
    """Change the published node of a pipe"""
    await common_pipe_publish_node(ctx, pipe_name_or_id, node_uid)


@pipe.command(name="unpublish")
@click.argument('pipe_name_or_id')
@click.argument('node_uid', default=None, required=False)
@click.pass_context
@coro
async def pipe_unpublish_node(ctx, pipe_name_or_id, node_uid=None):
    """Unpublish the endpoint of a pipe"""
    client = ctx.obj['client']
    host = ctx.obj['config'].get('host', DEFAULT_API_HOST)

    try:
        pipe = await client.pipe(pipe_name_or_id)

        if not pipe['endpoint']:
            raise click.ClickException(FeedbackManager.error_remove_no_endpoint())

        if not node_uid:
            node = pipe['endpoint']
            click.echo(FeedbackManager.info_using_node(node=node))
        else:
            node = node_uid

        await client.pipe_remove_endpoint(pipe_name_or_id, node)
        click.echo(FeedbackManager.success_node_unpublished(pipe=pipe_name_or_id, host=host))
    except DoesNotExistException:
        raise click.ClickException(FeedbackManager.error_pipe_does_not_exist(pipe=pipe_name_or_id))
    except Exception as e:
        raise click.ClickException(FeedbackManager.error_exception(error=e))


@pipe.command(name="set_endpoint")
@click.argument('pipe_name_or_id')
@click.argument('node_uid', default=None, required=False)
@click.pass_context
@coro
async def pipe_published_node(ctx, pipe_name_or_id, node_uid=None):
    """Same as 'publish', change the published node of a pipe"""
    await common_pipe_publish_node(ctx, pipe_name_or_id, node_uid)


@pipe.command(name="rm")
@click.argument('pipe_name_or_id')
@click.option('--yes', is_flag=True, default=False, help="Do not ask for confirmation")
@click.pass_context
@coro
async def pipe_delete(ctx, pipe_name_or_id, yes):
    """Delete a pipe"""

    client = ctx.obj['client']

    if yes or click.confirm(FeedbackManager.warning_confirm_delete_pipe(pipe=pipe_name_or_id)):
        try:
            await client.pipe_delete(pipe_name_or_id)
        except DoesNotExistException:
            raise click.ClickException(FeedbackManager.error_pipe_does_not_exist(pipe=pipe_name_or_id))

        click.echo(FeedbackManager.success_delete_pipe(pipe=pipe_name_or_id))


@pipe.command(name="token_read")
@click.argument('pipe_name')
@click.pass_context
@coro
async def pipe_token_read(ctx, pipe_name):
    """Retrieve a token to read a pipe"""
    client = ctx.obj['client']

    try:
        await client.pipe_file(pipe_name)
    except DoesNotExistException:
        raise click.ClickException(FeedbackManager.error_pipe_does_not_exist(pipe=pipe_name))

    tokens = await client.tokens()
    token = None

    for t in tokens:
        for scope in t['scopes']:
            if scope['type'] == 'PIPES:READ' and scope['resource'] == pipe_name:
                token = t['token']
    if token:
        click.echo(token)
    else:
        click.echo(FeedbackManager.warning_token_pipe(pipe=pipe_name))


@pipe.command(name="data", context_settings=dict(
    allow_extra_args=True,
    ignore_unknown_options=True,
))
@click.argument('pipe')
@click.option('--query', default=None, help="Run SQL over pipe results")
@click.option('--format', 'format_', type=click.Choice(['json', 'csv'], case_sensitive=False), default='json', help="Return format (CSV, JSON)")
@click.pass_context
@coro
async def print_pipe(ctx: Context, pipe: str, query: str, format_: str):
    """Print data returned by a pipe

    Syntax: tb pipe data <pipe_name> --param_name value --param2_name value2 ...
    """

    client: TinyB = ctx.ensure_object(dict)['client']
    params = {ctx.args[i][2:]: ctx.args[i + 1] for i in range(0, len(ctx.args), 2)}
    req_format = 'json' if not format_ else format_.lower()
    try:
        res = await client.pipe_data(pipe, format=req_format, sql=query, params=params)
    except Exception as e:
        click.echo(FeedbackManager.error_exception(error=str(e)))
        return

    if not format_:
        stats = res['statistics']
        seconds = stats['elapsed']
        rows_read = humanfriendly.format_number(stats['rows_read'])
        bytes_read = humanfriendly.format_size(stats['bytes_read'])

        click.echo(FeedbackManager.success_print_pipe(pipe=pipe))
        click.echo(FeedbackManager.info_query_stats(seconds=seconds, rows=rows_read, bytes=bytes_read))
        print_data_table(res)
        click.echo('\n')
    else:
        click.echo(res)


@pipe.command(name="regression-test", short_help="Run regression tests using last requests")
@click.option('--prefix', default='', help="Use prefix for all the resources")
@click.option('--debug', is_flag=True, default=False, help="Prints internal representation, can be combined with any command to get more information.")
@click.option('--only-response-times', is_flag=True, default=False, help="Checks only response times")
@click.argument('filenames', type=click.Path(exists=True), nargs=-1, default=None)
@click.option('--workspace_map', nargs=2, type=str, multiple=True)
@click.option('--workspace', nargs=2, type=str, multiple=True, help="add a workspace path to the list of external workspaces, usage: --workspace name path/to/folder")
@click.option('--no-versions', is_flag=True, default=False, help="when set, resource dependency versions are not used, it pushes the dependencies as-is")
@click.option('-l', '--limit', type=click.IntRange(0, 100), default=0, required=False, help="Number of requests to validate")
@click.option('--sample-by-params', type=click.IntRange(1, 100), default=1, required=False, help="When set, we will aggregate the pipe_stats_rt requests by extractURLParameterNames(assumeNotNull(url)) and for each combination we will take a sample of N requests")
@click.option('-m', '--match', multiple=True, required=False, help="Filter the checker requests by specific parameter. You can pass multiple parameters -m foo -m bar")
@click.option('-ff', '--failfast', is_flag=True, default=False, help="When set, the checker will exit as soon one test fails")
@click.option('--ignore-order', is_flag=True, default=False, help="When set, the checker will ignore the order of list properties")
@click.pass_context
@coro
async def regression_test(
        ctx: click.Context,
        prefix: str,
        filenames: Path,
        debug: bool,
        only_response_times: bool,
        workspace_map,
        workspace: str,
        no_versions: bool,
        limit: int,
        sample_by_params: int,
        match: List[str],
        failfast: bool,
        ignore_order: bool):
    """Run regression tests on Tinybird
    """

    ignore_sql_errors = FeatureFlags.ignore_sql_errors()

    context.disable_template_security_validation.set(True)
    await folder_push(
        create_tb_client(ctx),
        prefix,
        filenames,
        dry_run=False,
        check=True,
        push_deps=False,
        debug=debug,
        force=False,
        populate=False,
        upload_fixtures=False,
        wait=False,
        ignore_sql_errors=ignore_sql_errors,
        skip_confirmation=False,
        only_response_times=only_response_times,
        workspace_map=dict(workspace_map),
        workspace_lib_paths=workspace,
        no_versions=no_versions,
        timeout=False,
        run_tests=True,
        tests_to_run=limit,
        tests_sample_by_params=sample_by_params,
        tests_filter_by=match,
        tests_failfast=failfast,
        tests_ignore_order=ignore_order
    )
    return


@cli.command(short_help="Drop all the resources inside a project with prefix. This command is dangerous because it removes everything, use with care")  # noqa: C901
@click.argument('prefix')
@click.option('--yes', is_flag=True, default=False, help="Do not ask for confirmation")
@click.option('--dry-run', is_flag=True, default=False, help="Run the command without removing anything")
@click.pass_context
@coro
async def drop_prefix(ctx, prefix, yes, dry_run):  # noqa: C901
    """Drop all the resources inside a project with prefix. This command is dangerous because it removes everything, use with care"""

    if yes or click.confirm(FeedbackManager.warning_confirm_drop_prefix(prefix=prefix)):
        filenames = get_project_filenames(getcwd())
        context.disable_template_security_validation.set(True)
        resources, dep_map = await build_graph(filenames, create_tb_client(ctx), process_dependencies=True)
        names = [r['resource_name'].replace(".", "_") for r in resources.values()]
        res = {}
        client = ctx.obj['client']

        pipes = await client.pipes()
        for pipe in pipes:
            tk = get_name_tag_version(pipe['name'])
            if tk['tag'] == prefix and tk['name'] in names:
                res[tk['name']] = pipe['name']

        for group in reversed(list(toposort(dep_map))):
            for name in group:
                if name in res:
                    if resources[name]['resource'] == 'datasources':
                        if not dry_run:
                            click.echo(FeedbackManager.info_removing_datasource(datasource=res[name]))
                            try:
                                await client.datasource_delete(res[name])
                            except DoesNotExistException:
                                click.echo(FeedbackManager.info_removing_datasource_not_found(datasource=res[name]))
                            except CanNotBeDeletedException as e:
                                click.echo(FeedbackManager.error_datasource_can_not_be_deleted(datasource=res[name], error=e))
                            except Exception as e:
                                raise click.ClickException(FeedbackManager.error_exception(error=e))
                        else:
                            click.echo(FeedbackManager.info_dry_removing_datasource(datasource=res[name]))
                    else:
                        if not dry_run:
                            click.echo(FeedbackManager.info_removing_pipe(pipe=res[name]))
                            try:
                                await client.pipe_delete(res[name])
                            except DoesNotExistException:
                                click.echo(FeedbackManager.info_removing_pipe_not_found(pipe=res[name]))
                        else:
                            click.echo(FeedbackManager.info_dry_removing_pipe(pipe=res[name]))

        ds = await client.datasources()
        for t in ds:
            tk = get_name_tag_version(t['name'])
            if tk['tag'] == prefix and tk['name'] in names:
                res[tk['name']] = t['name']
                if not dry_run:
                    click.echo(FeedbackManager.info_removing_datasource(datasource=t['name']))
                    try:
                        await client.datasource_delete(t['name'])
                    except DoesNotExistException:
                        click.echo(FeedbackManager.info_removing_datasource_not_found(datasource=t['name']))
                    except CanNotBeDeletedException as e:
                        click.echo(FeedbackManager.error_datasource_can_not_be_deleted(datasource=t['name'], error=e))
                    except Exception as e:
                        raise click.ClickException(FeedbackManager.error_exception(error=e))
                else:
                    click.echo(FeedbackManager.info_dry_removing_datasource(datasource=t['name']))


@cli.group()
@click.pass_context
def job(ctx):
    '''Jobs commands'''


@job.command(name="ls")
@click.option('-s', '--status', help="Show only jobs with this status",
              type=click.Choice(['waiting', 'working', 'done', 'error'], case_sensitive=False),
              multiple=True, default=None)
@click.pass_context
@coro
async def jobs_ls(ctx, status):
    """List jobs"""
    client = ctx.obj['client']
    jobs = await client.jobs(status=status)
    columns = ['id', 'kind', 'status', 'created at', 'updated at', 'job url']
    click.echo(FeedbackManager.info_jobs())
    table = []
    for j in jobs:
        table.append([j[c.replace(' ', '_')] for c in columns])
    click.echo(humanfriendly.tables.format_smart_table(table, column_names=columns))
    click.echo('\n')


@job.command(name="details")
@click.argument('job_id')
@click.pass_context
@coro
async def job_details(ctx, job_id):
    """Get details for a job"""
    client = ctx.obj['client']
    job = await client.job(job_id)
    columns = []
    click.echo(FeedbackManager.info_job(job=job_id))
    table = []
    columns = job.keys()
    table = [job.values()]
    click.echo(humanfriendly.tables.format_smart_table(table, column_names=columns))
    click.echo('\n')


@job.command(name="cancel")
@click.argument('job_id')
@click.pass_context
@coro
async def job_cancel(ctx, job_id):
    """Try to cancel a Job"""
    client = ctx.obj['client']

    try:
        result = await client.job_cancel(job_id)
    except DoesNotExistException:
        click.echo(FeedbackManager.error_job_does_not_exist(job_id=job_id))
    except Exception as e:
        click.echo(FeedbackManager.error_exception(error=e))
    else:
        current_job_status = result['status']
        if current_job_status == 'cancelling':
            click.echo(FeedbackManager.success_job_cancellation_cancelling(job_id=job_id))
        elif current_job_status == 'cancelled':
            click.echo(FeedbackManager.success_job_cancellation_cancelled(job_id=job_id))
        else:
            click.echo(FeedbackManager.error_job_cancelled_but_status_unknown(job_id=job_id))
    click.echo('\n')


@cli.group()
@click.pass_context
def connection(ctx):
    '''Connection commands'''


@connection.group(name="create")
@click.pass_context
def connection_create(ctx):
    '''Connection Create commands'''


@connection_create.command(name="kafka", short_help='Add a Kafka connection')
@click.option('--bootstrap-servers', help="Kafka Bootstrap Server in form mykafka.mycloud.com:9092")
@click.option('--key', help="Key")
@click.option('--secret', help="Secret")
@click.option('--connection-name', default=None, help="The name of your Kafka connection. If not provided, it's set as the bootstrap server")
@click.option('--auto-offset-reset', default=None, help="Offset reset, can be 'latest' or 'earliest'. Defaults to 'latest'.")
@click.option('--schema-registry-url', default=None, help="Avro Confluent Schema Registry URL")
@click.option('--sasl-mechanism', default=None, help="Authentication method for connection-based protocols. Defaults to 'PLAIN'")
@click.pass_context
@coro
async def connection_create_kafka(ctx, bootstrap_servers, key, secret, connection_name, auto_offset_reset, schema_registry_url, sasl_mechanism):
    """
    Add a Kafka connection

    \b
    $ tb connection create kafka --bootstrap-server google.com:80 --key a --secret b --connection-name c
    """

    bootstrap_servers and validate_kafka_bootstrap_servers(bootstrap_servers)
    key and validate_kafka_key(key)
    secret and validate_kafka_secret(secret)
    schema_registry_url and validate_kafka_schema_registry_url(schema_registry_url)
    auto_offset_reset and validate_kafka_auto_offset_reset(auto_offset_reset)

    if not bootstrap_servers:
        bootstrap_servers = click.prompt("Kafka Bootstrap Server")
        validate_kafka_bootstrap_servers(bootstrap_servers)
    if not key:
        key = click.prompt("Key")
        validate_kafka_key(key)
    if not secret:
        secret = click.prompt("Secret", hide_input=True)
        validate_kafka_secret(secret)
    if not connection_name:
        connection_name = click.prompt(f"Connection name (optional, current: {bootstrap_servers})", default=bootstrap_servers)

    client = ctx.obj['client']
    result = await client.connection_create_kafka(
        bootstrap_servers,
        key,
        secret,
        connection_name,
        auto_offset_reset,
        schema_registry_url,
        sasl_mechanism)

    id = result['id']
    click.echo(FeedbackManager.success_connection_created(id=id))


def validate_kafka_schema_registry_url(schema_registry_url):
    if not is_url_valid(schema_registry_url):
        raise click.ClickException(FeedbackManager.error_kafka_registry())


def is_url_valid(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def validate_kafka_bootstrap_servers(host_and_port):
    if not isinstance(host_and_port, str):
        raise click.ClickException(FeedbackManager.error_kafka_bootstrap_server())
    parts = host_and_port.split(":")
    if len(parts) > 2:
        raise click.ClickException(FeedbackManager.error_kafka_bootstrap_server())
    host = parts[0]
    port = parts[1] if len(parts) == 2 else "9092"
    try:
        port = int(port)
    except Exception:
        raise click.ClickException(FeedbackManager.error_kafka_bootstrap_server())
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        try:
            sock.settimeout(3)
            sock.connect((host, port))
        except socket.timeout:
            raise click.ClickException(FeedbackManager.error_kafka_bootstrap_server_conn_timeout())
        except Exception:
            raise click.ClickException(FeedbackManager.error_kafka_bootstrap_server_conn())


def validate_kafka_key(s):
    if not isinstance(s, str):
        raise click.ClickException("Key format is not correct, it should be a string")


def validate_kafka_secret(s):
    if not isinstance(s, str):
        raise click.ClickException("Password format is not correct, it should be a string")


@connection.command(name="rm")
@click.argument('connection_id')
@click.option('--force', default=False, help="Force connection removal even if there are datasources currently using it")
@click.pass_context
@coro
async def connection_rm(ctx, connection_id, force):
    """Remove a connection"""
    client = ctx.obj['client']
    try:
        await client.connector_delete(connection_id)
    except DoesNotExistException:
        raise click.ClickException(FeedbackManager.error_connection_does_not_exists(connection_id=connection_id))
    except Exception as e:
        raise click.ClickException(FeedbackManager.error_exception(error=e))
    click.echo(FeedbackManager.success_delete_connection(connection_id=connection_id))


@connection.command(name="ls")
@click.option('--connector', help="Filter by connector")
@click.pass_context
@coro
async def connection_ls(ctx, connector):
    from tinybird.connectors import DataConnectorSettings, DataSensitiveSettings

    """List connections"""
    client = ctx.obj['client']
    connections = await client.connections(connector=connector)
    columns = []
    table = []

    click.echo(FeedbackManager.info_connections())

    if not connector:
        sensitive_settings = []
        columns = ['service', 'name', 'id', 'connected_datasources']
    else:
        sensitive_settings = getattr(DataSensitiveSettings, connector)
        columns = ['service', 'name', 'id', 'connected_datasources'] + [setting.replace('tb_', '') for setting in getattr(DataConnectorSettings, connector)]

    for connection in connections:
        row = [_get_setting_value(connection, setting, sensitive_settings) for setting in columns]
        table.append(row)

    column_names = [c.replace('kafka_', '') for c in columns]
    click.echo(humanfriendly.tables.format_smart_table(table, column_names=column_names))
    click.echo('\n')


def _get_setting_value(connection, setting, sensitive_settings):
    if setting in sensitive_settings:
        return '*****'
    return connection.get(setting, '')


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


if __name__ == '__main__':
    cli()
