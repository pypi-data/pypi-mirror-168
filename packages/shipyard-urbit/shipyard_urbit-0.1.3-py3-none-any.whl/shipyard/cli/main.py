import os
from pathlib import Path
from rich import print
import typer

from shipyard.api.main import gunicorn_full, gunicorn_local, uvicorn_local
from shipyard.db import connect_database
from shipyard.envoy.tunnel import open_tunnel
from shipyard.models import SshRemote
from shipyard.settings import get_settings, load_settings, DEFAULT_DATA_DIR


app = typer.Typer()


@app.callback(no_args_is_help=True)
def callback(
    data_dir: str = typer.Option(
        None,
        help="Directory containing the application database, will be created if necessary.",
        show_default=f"{DEFAULT_DATA_DIR}{os.sep}",  # pyright:ignore
    ),
):
    """
    Urbit hosting and automation platform

    Global options must be entered before a command.
    """
    if data_dir:
        load_settings(data_dir=data_dir)
    else:
        load_settings()

    ensure_data_dir()

    connect_database()


def ensure_data_dir():
    data_dir: Path = get_settings().data_dir

    if data_dir.is_file():
        print(f"Cannot access directory {data_dir}{os.sep}: It is a regular file.")
        raise typer.Exit(1)

    if data_dir.is_symlink() and not data_dir.exists():
        print(f"Cannot access directory {data_dir}{os.sep}: It is a broken link.")
        raise typer.Exit(1)

    if not data_dir.is_dir():
        proceed = typer.confirm(
            f"Create data directory?: {data_dir}{os.sep}",
            default=(data_dir == DEFAULT_DATA_DIR),
            abort=True,
        )
        if proceed:
            try:
                data_dir.mkdir()
            except Exception as e:
                print(f"Cannot create directory {data_dir}{os.sep}: {e}.")
                raise typer.Exit(1)


@app.command()
def api(
    host: str = typer.Option("127.0.0.1", help="Host the server will listen on"),
    port: int = typer.Option("8000", help="Port the server will listen on"),
    log_level: str = typer.Option("info", help="Logging level of the server"),
    dev: bool = typer.Option(
        False, help="Run a dev server that reloads on code changes"
    ),
):
    """
    Run a local API server
    """
    if dev:
        uvicorn_local(host=host, port=port, log_level=log_level, reload=True)
    else:
        gunicorn_local(host, port, log_level)


@app.command(
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True}
)
def gunicorn():
    """
    Run API in a custom Gunicorn app.

    Use for specialized deployments.  All command line options are passed
    directly to Gunicorn.

    Reference:
    https://docs.gunicorn.org/en/latest/settings.html
    """
    gunicorn_full()


@app.command(no_args_is_help=True)
def tunnel(
    host: str = typer.Option(
        ..., "--host", "-h", help="Hostname of the remote SSH server"
    ),
    user: str = typer.Option(
        ..., "--user", "-u", help="Username to login to remote SSH server"
    ),
    port: int = typer.Option(
        22, "--port", "-p", help="Listening port of the remote SSH server"
    ),
    local_port: int = typer.Option(
        4000, "--local-port", "-L", help="Local port to forward application to"
    ),
    remote_port: int = typer.Option(
        4000, "--remote-port", "-R", help="Remote application port to forward"
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Print additional status information"
    ),
):
    """
    Open an SSH tunnel to a remote ship, allowing you to connect on a local port
    """
    ssh: SshRemote = SshRemote(url=f"ssh://{user}@{host}:{port}")  # pyright:ignore
    open_tunnel(ssh, local_port, remote_port, verbose)
