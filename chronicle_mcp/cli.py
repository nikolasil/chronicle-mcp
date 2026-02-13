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


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx: click.Context) -> None:
    """ChronicleMCP - MCP server for secure local browser history access."""
    if ctx.invoked_subcommand is None:
        from chronicle_mcp.cli import run_command
        ctx.invoke(run_command)


@cli.command("version")
@click.pass_context
def version_command(ctx: click.Context) -> None:
    """Show the version of ChronicleMCP."""
    version = get_version()
    click.echo(f"ChronicleMCP version: {version}")


@cli.command("run")
@click.option(
    "--transport",
    type=click.Choice(["stdio", "sse"]),
    default="stdio",
    help="Transport mode for MCP communication",
)
@click.option(
    "--host",
    default="127.0.0.1",
    help="Host to bind HTTP server to (only for SSE transport)",
)
@click.option(
    "--port",
    type=int,
    default=8080,
    help="Port to bind HTTP server to (only for SSE transport)",
)
@click.pass_context
def run_command(ctx: click.Context, transport: str, host: str, port: int) -> None:
    """Run the ChronicleMCP server."""
    if transport == "stdio":
        from chronicle_mcp.protocols.mcp import mcp

        click.echo("Starting ChronicleMCP in stdio mode...")
        mcp.run()
    else:
        from chronicle_mcp.protocols.http import run_http_server

        click.echo(f"Starting ChronicleMCP in SSE mode on {host}:{port}...")
        run_http_server(host=host, port=port)


@cli.command("serve")
@click.option(
    "--host",
    default="127.0.0.1",
    help="Host to bind HTTP server to",
)
@click.option(
    "--port",
    type=int,
    default=8080,
    help="Port to bind HTTP server to",
)
@click.option(
    "--browser",
    default="chrome",
    help="Default browser to use",
)
@click.option(
    "--foreground/--daemon",
    default=True,
    help="Run in foreground or as daemon",
)
@click.pass_context
def serve_command(
    ctx: click.Context,
    host: str,
    port: int,
    browser: str,
    foreground: bool,
) -> None:
    """Start ChronicleMCP as a long-running HTTP/SSE server."""
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
            "serve",
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

    click.echo(f"Starting ChronicleMCP server on {host}:{port}")
    run_http_server(host=host, port=port, default_browser_=browser)


@cli.command("status")
@click.option(
    "--port",
    type=int,
    default=8080,
    help="Port to check",
)
@click.pass_context
def status_command(ctx: click.Context, port: int) -> None:
    """Check if the ChronicleMCP server is running."""
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


@cli.command("logs")
@click.option(
    "--port",
    type=int,
    default=8080,
    help="Port to get logs from",
)
@click.option(
    "--lines",
    type=int,
    default=50,
    help="Number of lines to show",
)
@click.pass_context
def logs_command(ctx: click.Context, port: int, lines: int) -> None:
    """Show logs from the ChronicleMCP server."""
    log_file = Path(tempfile.gettempdir()) / f"chronicle-mcp-{port}.log"

    if not log_file.exists():
        click.echo(f"No logs found for port {port}")
        return

    content = log_file.read_text()
    all_lines = content.split("\n")
    recent_lines = all_lines[-lines:] if lines else all_lines
    click.echo("\n".join(recent_lines))


@cli.command("completion")
@click.argument("shell", type=click.Choice(["bash", "zsh", "fish"]))
@click.pass_context
def completion_command(ctx: click.Context, shell: str) -> None:
    """Generate shell completion script."""
    if shell == "bash":
        click.echo("""#!/usr/bin/env bash
# chronicle-mcp bash completion

_chronicle_mcp_completions() {
    local cur prev words cword
    _init_completion || return
    if [[ "$cur" == "--"* ]]; then
        COMPREPLY=( $(compgen -W "--help --version --transport --host --port --browser" -- "$cur") )
    else
        COMPREPLY=( $(compgen -W "run serve status logs completion version" -- "$cur") )
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
        "--transport:Transport mode (stdio or sse)"
        "--host:Host to bind"
        "--port:Port to bind"
        "--browser:Default browser"
    )
    _describe -t command 'chronicle-mcp command' options
}
compdef _chronicle_mcp chronicle-mcp
""")
    elif shell == "fish":
        click.echo("""# chronicle-mcp fish completion
complete -c chronicle-mcp -f -a "(chronicle-mcp run serve status logs completion version)"
complete -c chronicle-mcp -l help -d "Show help"
complete -c chronicle-mcp -l version -d "Show version"
complete -c chronicle-mcp -l transport -d "Transport mode" -a "stdio sse"
complete -c chronicle-mcp -l host -d "Host to bind"
complete -c chronicle-mcp -l port -d "Port to bind"
complete -c chronicle-mcp -l browser -d "Default browser"
""")


@cli.command("list-browsers")
@click.pass_context
def list_browsers_command(ctx: click.Context) -> None:
    """List available browsers on the system."""
    browsers = get_available_browsers()
    if browsers:
        click.echo("Available browsers:")
        for browser in browsers:
            click.echo(f"  - {browser}")
    else:
        click.echo("No browsers with history found on this system")
