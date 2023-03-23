from typing import List


def formatted_requirements_list(requirements):
    return "\\n".join([f"- {r}" for r in requirements])


def write_commands_and_options_spec_prompt(
    requirements: List[str],
    file_name: str,
    command_and_options: str,
):
    prompt = f"""We are writing a CLI that will fulfill the following requirements:

{formatted_requirements_list(requirements)}

We are currently implementing this command:

{command_and_options}

We are using click to implement the CLI. The file we are working on is `{file_name}` and it currently looks like this:

```
import click

@cli.command(name="command")
@click.argument(
    "example"
)
@click.option(
    "-o",
    "--option",
    help="An example option",
)
def first_command(example, option):
    "Command description goes here"
    click.echo("Here is some output")
```

Can you rewrite the file to implememt the commands and options? Return the output in a code block.
"""

    return {
        "role": "user",
        "content": prompt,
    }
