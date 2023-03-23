from typing import List
from .utils import default_json_output_instructions


def write_method_test_signatures_prompt(method_implementation: str):
    prompt = f"""
            For this given method implementation, write only the signatures for possible tests:
        {method_implementation}

        {default_json_output_instructions}
        e.g. [{{"test_signature": "...", "test_comment": "...}}] 

    """, 

    return [{
            "role": "user",
            "content": prompt,
            }]
