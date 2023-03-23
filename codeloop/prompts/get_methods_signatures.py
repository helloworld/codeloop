from typing import List
from .utils import default_json_output_instructions


def get_methods_signatures_for_commands_prompt(commands_list: List[str]):
    prompt = f"""For these CLI commands, write all the method signatures that we would need to implement them:

{commands_list}

Think step by step first.

{default_json_output_instructions}

e.g. [{{"method_signature": "..."}}]"""

    return [
        {
            "role": "user",
            "content": prompt,
        }
    ]
