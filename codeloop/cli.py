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
            "encode a string using base6",
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
        subprocess.run(cookiecutter_cmd, check=True)
    except subprocess.CalledProcessError as e:
        console.print(f"Error executing cookiecutter: {e}", style="bold red")
        return

    controller = ChatGPTController(package_name, requirements, relative_path)
    controller.run_codeloop()



if __name__ == "__main__":
    cli()
