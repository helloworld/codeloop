import subprocess
import click
from rich.prompt import Prompt
from rich.panel import Panel

from codeloop.chatgpt_controller import ChatGPTController
from codeloop.console import console


@click.group()
@click.version_option()
def cli():
    """An AI tool to generate CLIs"""


@cli.command(name="generate")
@click.option("--demo", is_flag=True, help="Generate a demo package")
def generate(demo):
    console.print("codeloop generate", style="bold")

    if demo:
        console.print("Generating demo package...", style="bold green")
        package_name = "basecoder"
        requirements = [
            "encode a string using base64",
            "decode a string using base64",
            "for both encode and decode, specify a different base as an option",
        ]
    else:
        package_name = Prompt.ask("What do you want the name of the package to be?")
        console.print(f"> {package_name}")

        requirements = []
        while True:
            requirement = Prompt.ask(
                "What are the set of requirements for the package? (type 'done' to finish)"
            )
            if requirement.lower() == "done":
                break
            requirements.append(requirement)
            console.print(f"> {requirement}")

        console.print("\nPackage generated successfully!", style="bold green")

    relative_path = f"./{package_name}"
    package_info = f"Package Name: [bold]{package_name}[/bold]\n\nRequirements:\n"
    for requirement in requirements:
        package_info += f"- {requirement}\n"
    package_info += f"\nRelative Path: [bold]{relative_path}[/bold]"

    panel = Panel(package_info, title="Package Information", border_style="blue")
    console.print(panel)

    try:
        console.print(
            f"[bold][red]Existing directory found. Deleting directory {relative_path}...[/red][/bold]"
        )
        subprocess.run(["rm", "-rf", relative_path], check=True)
    except subprocess.CalledProcessError as e:
        console.print(f"Error deleting directory: {e}", style="bold red")
        return

    cookiecutter_template = "gh:simonw/click-app"
    cookiecutter_cmd = [
        "cookiecutter",
        cookiecutter_template,
        f"--no-input",
        f"app_name={package_name}",
        f"description={package_name}",
        f"hyphenated={package_name}",
        f"underscored={package_name}",
        f"github_username={package_name}",
        f"author_name={package_name}",
    ]

    try:
        console.print(
            f"[bold][red]Generating package using cookiecutter...[/red][/bold]"
        )
        subprocess.run(cookiecutter_cmd, check=True)
    except subprocess.CalledProcessError as e:
        console.print(f"Error executing cookiecutter: {e}", style="bold red")
        return

    try:
        console.print(f"[bold][red]Installing package...[/red][/bold]")
        subprocess.run(["pip", "install", "-e", "."], check=True, cwd=relative_path)
    except subprocess.CalledProcessError as e:
        console.print(f"Error installing package: {e}", style="bold red")
        return



    controller = ChatGPTController(package_name, requirements, relative_path)
    base_cli_template ="""
import os
import click
import importlib

__globals = globals()

@click.group()
@click.version_option()
def cli():
    "basecoder"

for file in os.listdir(os.path.dirname(__file__)):
    mod_name = file[:-3]   # strip .py at the end
    print("module: ", mod_name)
    if mod_name.startswith('command_'):
        # mod_name_stripped = mod_name.split("basecoder.cli")
        # print("stripped: ", mod_name_stripped)
        mod = importlib.import_module('basecoder' + '.' + mod_name)
        __globals[mod_name] = mod
        functions_list = dir(mod)
        commands_functions_list = [f for f in functions_list if f.startswith('command_')]

        for cmd_name in commands_functions_list:
            func_mod = getattr(mod, cmd_name)
            cli.add_command(func_mod)
    """
    controller._write_file_to_project("cli.py", base_cli_template)
    controller.run_codeloop()


if __name__ == "__main__":
    cli()
