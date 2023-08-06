from typing import List, Optional
import typer
from src.auth import Auth
from src.client import ArvanClient

app = typer.Typer()


@app.command()
def authenticate(
    api_key: str = typer.Option(..., prompt=True, hide_input=True,
                                help="Set your API key. Keep in mind that it will be stored in plain text."),
):
    """
    Add API key
    """
    Auth.create(api_key)


@app.command()
def ls():
    """
    List all servers
    """
    if not Auth.exists():
        typer.echo("You need to authenticate first.")
        return
    client = ArvanClient(Auth.get())
    servers = client.get_all_servers()
    import json
    typer.echo(json.dumps(servers, indent=4))

@app.command()
def turn_on(
    all: bool = typer.Option(False, "--all", "-a",
                             help="Turn on all servers"),
) -> None:
    """
    Turn on server(s)
    """
    if not Auth.exists():
        typer.echo("You need to authenticate first.")
        return
    client = ArvanClient(Auth.get())
    if all:
        client.turn_on_all_servers()


@app.command()
def shutdown(
    all: bool = typer.Option(False, "--all", "-a",
                             help="Shutdown all servers"),
) -> None:
    """
    Shutdown server(s)
    """
    if not Auth.exists():
        typer.echo("You need to authenticate first.")
        return
    client = ArvanClient(Auth.get())
    if all:
        client.shutdown_all_servers()


def main() -> None:
    app()


if __name__ == "__main__":
    main()
