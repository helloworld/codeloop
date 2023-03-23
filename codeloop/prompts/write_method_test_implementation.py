from typing import List
from .utils import default_json_output_instructions


def write_method_test_implementation_prompt(method_test_signature: dict):
    prompt = f"""
        For this given test info, write only the test implementation:
        - test name: {method_test_signature["test_name"]}
        - test comment: {method_test_signature["test_comment"]}
        
        Return output inside a code block, with language specified.

    """, 

    return [{
            "role": "user",
            "content": prompt,
            }]
