import click
from codeloop.console import console

@click.group()
@click.version_option()
def cli():
    "An AI tool to generate CLIs"


@cli.command(name="generate")
def first_command():
    "Command description goes here"
    click.echo("Here is some output")
