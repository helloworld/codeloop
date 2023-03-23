from typing import List
from .utils import default_json_output_instructions


def write_method_body_implementation_prompt(method_signature_payload: dict):
    # TODO: can maybe also add original program-level requirements too if helpful
    prompt = f"""
        For this method signature, write the body implementation:
        {method_signature_payload["method_signature"]}

        Return output inside a code block.
    """, 

    return [{
            "role": "user",
            "content": prompt,
            }]
