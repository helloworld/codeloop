from typing import List


def formatted_requirements_list(requirements):
    return "\\n".join([f"- {r}" for r in requirements])


def write_commands_and_options_spec_prompt(
    requirements: List[str],
    file_name: str,
    command_and_options: str,
):
    prompt = f"""We are writing a CLI and currently implementing the following command: 

{command_and_options}

We are using click to implement the CLI. The file we are working on is `{file_name}` the output should look like this.

```
import click

@click.command(name="{command_and_options["command_name"]}")
@click.argument(
    "example"
)
@click.option(
    "-o",
    "--option",
    help="An example option",
)
def command_{command_and_options['command_name']}(example, option):
    "Command description goes here"
    click.echo("Here is some output")
```

Can you rewrite the file to implememt the commands and options? Return the output in a code block. Do not implement the command group.

Make sure the method is named `command_{command_and_options['command_name']}` and that the command name is `{command_and_options['command_name']}`.

Output:
"""

    return {
        "role": "user",
        "content": prompt,
    }
