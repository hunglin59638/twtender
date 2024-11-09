#!/usr/bin/env python
import click
import uvicorn
import importlib.metadata

_DISTRIBUTION_METADATA = importlib.metadata.metadata("twtender")
VERSION = _DISTRIBUTION_METADATA["version"]


@click.command(help="Run the twtender API server.")
@click.option("-v", "--version", is_flag=True, help="Show the version and exit.")
@click.option(
    "-p", "--port", default=8000, show_default=True, help="Port to run the server on."
)
def main(version, port):
    if version:
        click.echo(f"twtender v{VERSION}")
        return
    uvicorn.run("twtender.api:app", workers=4, host="0.0.0.0", port=port, reload=False)


if __name__ == "__main__":
    main()
