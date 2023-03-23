import click
from rich.console import Console
from rich.prompt import Prompt

from codeloop.chatgpt_controller import ChatGPTController

console = Console()


@click.group()
@click.version_option()
def cli():
    """An AI tool to generate CLIs"""


@cli.command(name="generate")
def generate():
    console.print("codeloop generate", style="bold")

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

    controller = ChatGPTController(package_name, requirements, relative_path)


if __name__ == "__main__":
    cli()
