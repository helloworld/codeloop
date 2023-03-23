from typing import List
import openai
from rich.panel import Panel
from rich.pretty import Pretty
from codeloop.console import console
from rich.panel import Panel
import re
import json

from codeloop.prompts.get_commands_and_options_spec import (
    generate_commands_and_options_spec_prompt,
)
from codeloop.prompts.write_commands_and_options import (
    write_commands_and_options_spec_prompt,
)
from codeloop.prompts.get_methods_signatures import (
    get_methods_signatures_for_commands_prompt,
)
from codeloop.prompts.write_method_test_signatures import (
    write_method_test_signatures_prompt,
)
from codeloop.prompts.write_method_body_implementation import (
    write_method_body_implementation_prompt,
)
from codeloop.prompts.write_method_test_implementation import (
    write_method_test_implementation_prompt,
)


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
        for command_and_options in commands_and_options:
            command_name = command_and_options["command_name"]
            file_name = f"command_{command_name}.py"

            messages = [
                write_commands_and_options_spec_prompt(
                    self.requirements, file_name, command_and_options
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

    def get_methods_signatures_for_commands(self, commands_list):
        messages = get_methods_signatures_for_commands_prompt(commands_list)
        methods_signatures_list = self._request_completion(
            messages,
            extract_code_blocks=True,
            extract_jsons=True,
            include_lang=True,
            print_prompt=True,
        )
        return methods_signatures_list

    def write_method_body_implementation(self, method_signature_payload):
        method_body = self._request_completion(
            messages=write_method_body_implementation_prompt(method_signature_payload),
            extract_code_blocks=True,
            include_lang=True,
            print_prompt=True,
        )
        return method_body

    def write_method_test_signatures(self, method_implementation):
        test_signatures_list = self._request_completion(
            write_method_test_signatures_prompt(method_implementation),
            extract_code_blocks=True,
            include_lang=True,
            print_prompt=True,
        )
        return test_signatures_list

    def write_method_test_implementation(self, method_test_signature):
        test_implementation_code = self._request_completion(
            write_method_test_implementation_prompt(method_test_signature),
            extract_code_blocks=True,
            include_lang=True,
            print_prompt=True,
        )

        return test_implementation_code

    # Main code
    def run_codeloop(self):
        print("--Starting codeloop")

        commands_and_options_spec = self.get_commands_and_options_spec()

        self.write_commands_and_options_to_file(commands_and_options_spec)

        print("get_methods_signatures_for_commands")
        methods_signatures_list = self.get_methods_signatures_for_commands(
            commands_and_options_spec
        )

        print("--Iterate through all methods")
        for method_signature in methods_signatures_list:
            print("write_method_body_implementation")
            method_implementation = self.write_method_body_implementation(
                method_signature
            )

            print("write_method_test_signatures")
            test_signatures = self.write_method_test_signatures(method_implementation)

            all_method_tests = []
            print("--Iterate through all tests")
            for test_sig in test_signatures:
                print("write_method_test_implementation")
                method_test_implementation = self.write_method_test_implementation(
                    test_sig
                )
                all_method_tests.append(method_test_implementation)

            has_failures = False
            # Iterate till all tests are fixed and pass
            for test in all_method_tests:
                # TODO: figure out main loop
                continue

        print("Code is fully written")

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
                max_tokens=3500,
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
