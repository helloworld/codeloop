from typing import List


def generate_commands_and_options_spec_prompt(requirements: List[str]):
    prompt = f"""Generate the CLI commands for a CLI tool that will fulfill the following requirements:
{requirements}

Explain each command you want to generate, and the options for each command.

After the explanation, return the final output as a JSON list inside a code block using the following format:

```json 
[{{"command_name": "...",  [{{"option_name": "...", "option_description": "...}}]}}]
```

To explain the above structure, it's a list of commands, and for each command, we have a list of options. Each option has a name and a description:
"""

    return {
        "role": "user",
        "content": prompt,
    }
