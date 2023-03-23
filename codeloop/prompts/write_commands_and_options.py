from typing import List


def write_commands_and_options_spec_prompt(
    requirements: List[str], commands_and_options: str, file_to_rewrite_contents: str
):
    prompt = f"""We are writing a CLI that will fulfill the following requirements:
{requirements}

Here are the commands we want to generate, and the options for each command.

{commands_and_options}

Here is the file we want to rewrite:

```
{file_to_rewrite_contents}
```

Can you rewrite the file to implememt the commands and options? Do not implement the method body of the commands, but just write the method signatures. Write `pass` in the method body.
"""

    return {
        "role": "user",
        "content": prompt,
    }
