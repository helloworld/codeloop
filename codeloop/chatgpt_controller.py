import subprocess
from typing import List
import openai
from rich.panel import Panel
from rich.pretty import Pretty
from codeloop.console import console
from rich.panel import Panel
import re
import json
from codeloop.prompts.debug_tests import debug_tests_prompt

from codeloop.prompts.get_commands_and_options_spec import (
    generate_commands_and_options_spec_prompt,
)
from codeloop.prompts.write_commands_and_options import (
    write_commands_and_options_spec_prompt,
)
from codeloop.prompts.write_tests import write_tests_prompt


DEBUG = True


class CodeBlockError(Exception):
    pass


class ChatGPTController:
    def __init__(self, package_name, requirements, relative_path):
        self.package_name = package_name
        self.requirements = requirements
        self.relative_path = relative_path
        self.system_messages = [
            {
                "role": "system",
                "content": "You are an expert Python programmer who has tasteful design for Python architecture and package structure. You primarily respond in code blocks and JSON. ",
            },
        ]

    def _read_file_from_project(self, file_name):
        with open(f"{self.relative_path}/{self.package_name}/{file_name}", "r") as f:
            return f.read()

    def _write_file_to_project(self, file_name, file_contents):
        full_file_name = f"{self.relative_path}/{self.package_name}/{file_name}"
        print("writing to ", full_file_name)
        with open(full_file_name, "w") as f:
            f.write(file_contents)

    def _write_test_to_project(self, file_name, file_contents):
        with open(f"{self.relative_path}/tests/{file_name}", "w") as f:
            f.write(file_contents)

    def get_commands_and_options_spec(self):
        messages = [
            generate_commands_and_options_spec_prompt(self.requirements),
        ]
        commands_and_options_spec = None
        latest_error = None
        for i in range(3):
            try:
                commands_and_options_spec = self._request_completion(
                    messages,
                    extract_code_blocks=True,
                    extract_jsons=True,
                    include_lang=True,
                    print_prompt=True,
                )
            except CodeBlockError as e:
                # retry
                print("Retrying ", i)
                latest_error = e
                continue
            break

        if commands_and_options_spec is None:
            raise latest_error

        return commands_and_options_spec

    def write_commands_and_options_to_file(
        self,
        commands_and_options: str,
    ):
        for command_and_option in commands_and_options:
            command_name = command_and_option["command_name"]
            file_name = f"command_{command_name}.py"

            messages = [
                write_commands_and_options_spec_prompt(
                    self.requirements, file_name, command_and_option
                )
            ]

            rewritten_contents = self._request_completion(
                messages,
                extract_code_blocks=True,
                include_lang=True,
                print_prompt=True,
            )

            if rewritten_contents:
                self._write_file_to_project(file_name, rewritten_contents)

    def write_tests(self, commands_and_options: str):
        for command_and_option in commands_and_options:
            command_name = command_and_option["command_name"]
            command_file_name = f"command_{command_name}.py"
            test_file_name = f"test_command_{command_name}.py"
            command_implementation = self._read_file_from_project(command_file_name)

            messages = [write_tests_prompt(self.requirements, command_implementation)]

            contents = self._request_completion(
                messages,
                extract_code_blocks=True,
                include_lang=True,
                print_prompt=True,
            )

            if contents:
                self._write_test_to_project(test_file_name, contents)

    def debug_tests(self, commands_and_options: str):
        for command_and_option in commands_and_options:
            command_name = command_and_option["command_name"]
            command_file_name = f"command_{command_name}.py"
            test_file_name = f"test_command_{command_name}.py"
            command_implementation = self._read_file_from_project(command_file_name)

            tests_failed = True
            attempts = 0
            max_attempts = 5
            while tests_failed and attempts < max_attempts:
                attempts += 1
                try:
                    pytest_output = subprocess.check_output(
                        ["pytest", f"{self.relative_path}/tests/{test_file_name}"],
                        stderr=subprocess.STDOUT,
                    )

                    if pytest_output.decode("utf-8").find("FAILED") != -1:
                        tests_failed = True
                    else:
                        tests_failed = False

                except subprocess.CalledProcessError as e:
                    pytest_output = e.output

                if tests_failed:
                    console.print(
                        Panel.fit(
                            Pretty(pytest_output.decode("utf-8")),
                            title="Pytest Output",
                            border_style="red",
                        ),
                    )
                    messages = [
                        debug_tests_prompt(command_implementation, pytest_output)
                    ]

                    contents = self._request_completion(
                        messages,
                        extract_code_blocks=True,
                        include_lang=True,
                        print_prompt=True,
                        max_tokens=2000,
                    )

                    if contents:
                        self._write_test_to_project(command_file_name, contents)

    # Main code
    def run_codeloop(self):
        print("--Starting codeloop")

        commands_and_options_spec = self.get_commands_and_options_spec()

        self.write_commands_and_options_to_file(commands_and_options_spec)
        self.write_tests(commands_and_options_spec)
        self.debug_tests(commands_and_options_spec)

    def _print_prompt(self, messages):
        console.print(
            Panel.fit(
                Pretty(messages),
                title="Prompt",
                border_style="blue",
            ),
        )

    def _request_completion(
        self,
        messages,
        extract_code_blocks=False,
        extract_jsons=False,
        include_lang=False,
        model="gpt-3.5-turbo",
        print_prompt=False,
        max_tokens=3500,
    ):
        if print_prompt:
            self._print_prompt(messages)

        ## TODO: Add retry logic
        def _request(
            messages,
            model,
            extract_code_blocks=False,
            extract_jsons=False,
            include_lang=False,
        ):
            completion = openai.ChatCompletion.create(
                model=model,
                messages=self.system_messages + messages,
                max_tokens=max_tokens,
            )

            response_text = completion.choices[0].message.content
            if DEBUG:
                console.print(
                    Panel.fit(
                        Pretty(response_text),
                        title="Intermediate Response",
                        border_style="red",
                    ),
                )

            if extract_code_blocks:
                if include_lang:
                    code_blocks = re.findall(
                        r"```(?:[a-zA-Z0-9_\-]+)?\n?(.*?)\n?```",
                        response_text,
                        re.DOTALL,
                    )
                else:
                    code_blocks = re.findall(
                        r"```\n?(.*?)\n?```", response_text, re.DOTALL
                    )

                if len(code_blocks) == 0:
                    print(f"No code blocks found in response: {response_text}")
                    raise CodeBlockError(
                        f"No code blocks found in response: {response_text}"
                    )

                if extract_jsons:
                    jsons = []
                    for code_block in code_blocks:
                        try:
                            jsons.append(json.loads(code_block.strip()))
                        except json.JSONDecodeError:
                            pass

                    if len(jsons) == 0:
                        print(f"Could not parse any JSON response: {response_text}")
                        raise CodeBlockError(
                            f"Could not parse any JSON from response: {response_text}"
                        )

                    return jsons

                return code_blocks

            return [response_text]

        response = _request(
            messages,
            model,
            extract_code_blocks=extract_code_blocks,
            extract_jsons=extract_jsons,
            include_lang=include_lang,
        )[0]

        if DEBUG:
            console.print(
                Panel.fit(
                    Pretty(response),
                    title="Final Response",
                    border_style="red",
                ),
            )

        return response
