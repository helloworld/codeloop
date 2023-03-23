from typing import List


def formatted_requirements_list(requirements):
    return "\\n".join([f"- {r}" for r in requirements])


def debug_tests_prompt(
    command_implementation: str,
    pytest_output: str,
):
    prompt = f"""We are writing a CLI and we implemented the following command for one of the requirements:

{command_implementation}

Here is the pytest output for the command:

{pytest_output}

Can you fix the code and reutrn the output in a code block? 
"""

    return {
        "role": "user",
        "content": prompt,
    }
