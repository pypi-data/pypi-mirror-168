import json
import sqlite3
import sys
from runpy import run_module, run_path

import click

from .config import load_config
from .db import load_trace_from_db, save_invocation_in_sqlite, setup_db
from .profiler import KoloProfiler


def get_profiler(one_trace_per_test) -> KoloProfiler:
    config = load_config()
    db_path = setup_db(config)
    return KoloProfiler(db_path, config=config, one_trace_per_test=one_trace_per_test)


def profile_module(profiler: KoloProfiler, module_name: str):
    with profiler:
        run_module(module_name, run_name="__main__", alter_sys=True)


def profile_path(profiler: KoloProfiler, path: str):
    with profiler:
        run_path(path, run_name="__main__")


@click.group()
def cli():
    """Base for all kolo command line commands"""

    # Ensure the current working directory is on the path.
    # Important when running the `kolo` script installed by setuptools.
    # Not really necessary when using `python -m kolo`, but doesn't hurt.
    # Note, we use 1, not 0: https://stackoverflow.com/q/10095037
    # This probably doesn't matter for our use case, but it doesn't hurt.
    sys.path.insert(1, ".")


@cli.command(context_settings={"ignore_unknown_options": True})
@click.argument("path")
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
@click.option("--one-trace-per-test", default=False, is_flag=True)
def run(path, args, one_trace_per_test):
    """
    Profile python code using kolo.

    PATH is the path to the python file or module being profiled.
    """
    if path == "python":
        path, *args = args
        if path == "-m":
            path, *args = args
            module = True
        else:
            module = False
    elif path.endswith(".py"):
        module = False
    else:
        module = True

    # Monkeypatch sys.argv, so the profiled code doesn't get confused
    # Without this, the profiled code would see extra args it doesn't
    # know how to handle.
    sys.argv = [path, *args]

    profiler = get_profiler(one_trace_per_test)
    try:
        if module:
            profile_module(profiler, path)
        else:
            profile_path(profiler, path)
    finally:
        if not one_trace_per_test:  # pragma: no branch
            profiler.save_request_in_db()


@cli.command()
@click.argument("path")
def load_trace(path):
    config = load_config()
    wal_mode = config.get("wal_mode", True)
    db_path = setup_db(config)

    try:
        with open(path) as dump:
            raw_data = dump.read()
    except FileNotFoundError:
        raise click.ClickException(f'File "{path}" not found')

    try:
        data = json.loads(raw_data)
    except json.JSONDecodeError:
        raise click.ClickException("Trace file is not valid json")
    try:
        trace_id = data["trace_id"]
    except KeyError:
        raise click.ClickException("Trace file is missing the `trace_id`")
    try:
        save_invocation_in_sqlite(
            db_path, trace_id, raw_data, wal_mode=wal_mode, ignore_errors=False
        )
    except sqlite3.IntegrityError:
        raise click.ClickException(f"Trace ID `{trace_id}` already exists")


@cli.command()
@click.argument("trace_id")
@click.option("--file", help="The name of the file to save the trace to.")
def dump_trace(trace_id, file):
    config = load_config()
    wal_mode = config.get("wal_mode", True)
    db_path = setup_db(config)

    try:
        data = load_trace_from_db(db_path, trace_id, wal_mode=wal_mode)
    except TypeError:
        raise click.ClickException(f"Could not find trace_id: `{trace_id}`")

    if file:
        with open(file, "w") as f:
            f.write(data)
    else:
        click.echo(data)


TEST_GENERATION_ERROR = """\
Test generation dependencies are not installed.

Run `pip install kolo[test_generation]` to install them.
"""


@cli.command()
@click.argument("trace_id")
@click.option("--test-name", default="test_my_view")
@click.option("--test-class", default="MyTestCase")
@click.option("--file", type=click.File("w"))
def generate_test(trace_id, test_name, test_class, file):
    try:
        from .generate_tests import generate_from_trace_id
    except ModuleNotFoundError:  # pragma: no cover
        raise click.ClickException(TEST_GENERATION_ERROR)

    test_code = generate_from_trace_id(trace_id, test_class, test_name)

    if file:
        file.write(test_code)
    else:
        click.echo(test_code)


if __name__ == "__main__":
    cli()  # pragma: no cover
