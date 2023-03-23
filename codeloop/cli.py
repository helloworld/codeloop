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
            "encode a string using base6",
            "decode a string using base64",
            "for both encode and decode, specify a different base as an option",
        ]
        relative_path = "./basecoder"
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

        relative_path = Prompt.ask("What is the relative path to write the project to?")
        console.print(f"> {relative_path}")

        console.print("\nPackage generated successfully!", style="bold green")

    package_info = f"Package Name: [bold]{package_name}[/bold]\n\nRequirements:\n"
    for requirement in requirements:
        package_info += f"- {requirement}\n"
    package_info += f"\nRelative Path: [bold]{relative_path}[/bold]"

    panel = Panel(package_info, title="Package Information", border_style="blue")
    console.print(panel)

    controller = ChatGPTController(package_name, requirements, relative_path)
    controller.get_commands_and_options()


if __name__ == "__main__":
    cli()
