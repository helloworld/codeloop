from typing import List


def formatted_requirements_list(requirements):
    return "\\n".join([f"- {r}" for r in requirements])


def generate_commands_and_options_spec_prompt(requirements: List[str]):
    prompt = f"""Generate the CLI commands for a CLI tool that will fulfill the following requirements:

{formatted_requirements_list(requirements)}

Return the output as a JSON list inside a code block using the following schema:

```json 
[
    {{
        "command_name": "...", "options": [{{"option_name": "...", "option_description": "...}}]
    }},
    {{
        "command_name": "...", "options": [{{"option_name": "...", "option_description": "...}}]
    }}
]
```
"""

    return {
        "role": "user",
        "content": prompt,
    }
