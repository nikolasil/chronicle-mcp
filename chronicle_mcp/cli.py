"""Command-line interface for ChronicleMCP."""

import logging
import os
import signal
import sys
import tempfile
from pathlib import Path

import click

from chronicle_mcp.config import get_version, setup_logging
from chronicle_mcp.paths import get_available_browsers

setup_logging()
logger = logging.getLogger(__name__)


@click.group()  # type: ignore[untyped-decorator]
@click.pass_context  # type: ignore[untyped-decorator]
def cli(ctx: click.Context) -> None:
    """ChronicleMCP - MCP server for secure local browser history access."""
    pass


@cli.command("version")  # type: ignore[untyped-decorator]
@click.pass_context  # type: ignore[untyped-decorator]
def version_command(ctx: click.Context) -> None:
    """Show the version of ChronicleMCP."""
    version = get_version()
    click.echo(f"ChronicleMCP version: {version}")


@cli.command("mcp")  # type: ignore[untyped-decorator]
@click.option(  # type: ignore[untyped-decorator]
    "--sse",
    is_flag=True,
    default=False,
    help="Use SSE (Server-Sent Events) transport instead of stdio",
)
@click.option(  # type: ignore[untyped-decorator]
    "--host",
    default="127.0.0.1",
    help="Host to bind to (only for SSE mode)",
)
@click.option(  # type: ignore[untyped-decorator]
    "--port",
    type=int,
    default=8080,
    help="Port to bind to (only for SSE mode)",
)
@click.pass_context  # type: ignore[untyped-decorator]
def mcp_command(ctx: click.Context, sse: bool, host: str, port: int) -> None:
    """Run the MCP server for AI assistants."""
    if sse:
        from chronicle_mcp.protocols.http import run_http_server

        click.echo(f"Starting ChronicleMCP MCP server (SSE) on {host}:{port}...")
        run_http_server(host=host, port=port)
    else:
        from chronicle_mcp.protocols.mcp import mcp

        click.echo("Starting ChronicleMCP MCP server (stdio)...")
        mcp.run()


@cli.command("http")  # type: ignore[untyped-decorator]
@click.option(  # type: ignore[untyped-decorator]
    "--host",
    default="127.0.0.1",
    help="Host to bind HTTP server to",
)
@click.option(  # type: ignore[untyped-decorator]
    "--port",
    type=int,
    default=8080,
    help="Port to bind HTTP server to",
)
@click.option(  # type: ignore[untyped-decorator]
    "--browser",
    default="chrome",
    help="Default browser to use",
)
@click.option(  # type: ignore[untyped-decorator]
    "--foreground/--daemon",
    default=True,
    help="Run in foreground or as daemon",
)
@click.pass_context  # type: ignore[untyped-decorator]
def http_command(
    ctx: click.Context,
    host: str,
    port: int,
    browser: str,
    foreground: bool,
) -> None:
    """Run the HTTP REST API server."""
    from chronicle_mcp.protocols.http import run_http_server

    pid_file = Path(tempfile.gettempdir()) / f"chronicle-mcp-{port}.pid"
    log_file = Path(tempfile.gettempdir()) / f"chronicle-mcp-{port}.log"

    if pid_file.exists():
        old_pid = pid_file.read_text().strip()
        try:
            os.kill(int(old_pid), 0)
            click.echo(f"Server already running with PID {old_pid}", err=True)
            sys.exit(1)
        except OSError:
            pid_file.unlink()

    if not foreground:
        import subprocess

        cmd = [
            sys.executable,
            "-m",
            "chronicle_mcp",
            "http",
            "--host",
            host,
            "--port",
            str(port),
            "--browser",
            browser,
            "--foreground",
        ]
        with open(log_file, "w") as f:
            subprocess.Popen(cmd, stdout=f, stderr=f)
        click.echo(f"Server started in background (PID file: {pid_file})")
        pid_file.write_text(str(os.getpid()))
        return

    def signal_handler(sig: int, frame: object) -> None:
        if pid_file.exists():
            pid_file.unlink()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    click.echo(f"Starting ChronicleMCP HTTP server on {host}:{port}")
    run_http_server(host=host, port=port, default_browser_=browser)


@cli.command("status")  # type: ignore[untyped-decorator]
@click.option(  # type: ignore[untyped-decorator]
    "--port",
    type=int,
    default=8080,
    help="Port to check",
)
@click.pass_context  # type: ignore[untyped-decorator]
def status_command(ctx: click.Context, port: int) -> None:
    """Check if the HTTP server is running."""
    pid_file = Path(tempfile.gettempdir()) / f"chronicle-mcp-{port}.pid"

    if not pid_file.exists():
        click.echo(f"ChronicleMCP is NOT running (no PID file at {pid_file})")
        return

    pid = pid_file.read_text().strip()
    try:
        os.kill(int(pid), 0)
        click.echo(f"ChronicleMCP is running (PID: {pid})")
    except OSError:
        click.echo(f"ChronicleMCP is NOT running (stale PID file, PID: {pid})")


@cli.command("logs")  # type: ignore[untyped-decorator]
@click.option(  # type: ignore[untyped-decorator]
    "--port",
    type=int,
    default=8080,
    help="Port to get logs from",
)
@click.option(  # type: ignore[untyped-decorator]
    "--lines",
    type=int,
    default=50,
    help="Number of lines to show",
)
@click.pass_context  # type: ignore[untyped-decorator]
def logs_command(ctx: click.Context, port: int, lines: int) -> None:
    """Show logs from the HTTP server."""
    log_file = Path(tempfile.gettempdir()) / f"chronicle-mcp-{port}.log"

    if not log_file.exists():
        click.echo(f"No logs found for port {port}")
        return

    content = log_file.read_text()
    all_lines = content.split("\n")
    recent_lines = all_lines[-lines:] if lines else all_lines
    click.echo("\n".join(recent_lines))


@cli.command("completion")  # type: ignore[untyped-decorator]
@click.argument("shell", type=click.Choice(["bash", "zsh", "fish"]))  # type: ignore[untyped-decorator]
@click.pass_context  # type: ignore[untyped-decorator]
def completion_command(ctx: click.Context, shell: str) -> None:
    """Generate shell completion script."""
    if shell == "bash":
        click.echo("""#!/usr/bin/env bash
# chronicle-mcp bash completion

_chronicle_mcp_completions() {
    local cur prev words cword
    _init_completion || return
    if [[ "$cur" == "--"* ]]; then
        COMPREPLY=( $(compgen -W "--help --version --host --port --browser --sse --foreground --daemon" -- "$cur") )
    else
        COMPREPLY=( $(compgen -W "mcp http status logs completion version list-browsers" -- "$cur") )
    fi
}
complete -F _chronicle_mcp_completions chronicle-mcp
""")
    elif shell == "zsh":
        click.echo("""#compdef chronicle-mcp
# chronicle-mcp zsh completion

_chronicle_mcp() {
    local -a options
    options=(
        "--help:Show help"
        "--version:Show version"
        "--host:Host to bind"
        "--port:Port to bind"
        "--browser:Default browser"
        "--sse:Use SSE transport"
    )
    _describe -t command 'chronicle-mcp command' options
}
compdef _chronicle_mcp chronicle-mcp
""")
    elif shell == "fish":
        click.echo("""# chronicle-mcp fish completion
complete -c chronicle-mcp -f -a "(chronicle-mcp mcp http status logs completion version list-browsers)"
complete -c chronicle-mcp -l help -d "Show help"
complete -c chronicle-mcp -l version -d "Show version"
complete -c chronicle-mcp -l host -d "Host to bind"
complete -c chronicle-mcp -l port -d "Port to bind"
complete -c chronicle-mcp -l browser -d "Default browser"
complete -c chronicle-mcp -l sse -d "Use SSE transport"
""")


@cli.command("list-browsers")  # type: ignore[untyped-decorator]
@click.pass_context  # type: ignore[untyped-decorator]
def list_browsers_command(ctx: click.Context) -> None:
    """List available browsers on the system."""
    browsers = get_available_browsers()
    if browsers:
        click.echo("Available browsers:")
        for browser in browsers:
            click.echo(f"  - {browser}")
    else:
        click.echo("No browsers with history found on this system")
