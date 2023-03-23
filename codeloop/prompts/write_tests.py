from typing import List


def formatted_requirements_list(requirements):
    return "\\n".join([f"- {r}" for r in requirements])


def write_tests_prompt(
    requirements: List[str],
    command_implementation: str,
):
    prompt = f"""We are writing a CLI that will fulfill the following requirements:

{formatted_requirements_list(requirements)}

We implemented the following command for one of the requirements:

{command_implementation}

We want to write tests to make sure that the command works as expected. Can you write the tests for this command? Return the output in a code block.

Here's an example of how to test the generic command:

```
from click.testing import CliRunner
from basecoder.cli import cli


def test_version():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert result.output.startswith("cli, version ")
```

Return the output in a code block.
"""

    return {
        "role": "user",
        "content": prompt,
    }
