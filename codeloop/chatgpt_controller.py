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

    def get_commands_and_options_spec(self):
        messages = self.system_messages + [
            generate_commands_and_options_spec_prompt(self.requirements),
        ]
        cli_spec_list = self._request_completion(
            messages,
            extract_code_blocks=True,
            extract_jsons=True,
            include_lang=True,
            print_prompt=True,
        )

        print("CLI command spec: ", cli_spec_list)
        return cli_spec_list

    def write_commands_and_options_spec_prompt(
        self,
        commands_and_options: str,
        file_to_rewrite: str,
    ):
        # Get the contents of file to rewrite at the {relative_path}/{package_name}/cli.py

        with open(
            f"{self.relative_path}/{self.package_name}/cli.py", "r"
        ) as file_to_rewrite:
            file_to_rewrite_contents = file_to_rewrite.read()

            messages = self.system_messages + [
                write_commands_and_options_spec_prompt(
                    self.requirements, commands_and_options, file_to_rewrite_contents
                )
            ]

            rewrite = self._request_completion(
                messages,
                extract_code_blocks=True,
                include_lang=True,
                print_prompt=True,
            )

            import pdb

            pdb.set_trace()

    def get_methods_signatures(self):
        # TODO
        return []

    def write_method_body_implementation(self, method_signature_payload):
        # TODO
        return ""

    def write_method_test_signatures(self, method_implementation):
        # TODO
        return []

    def write_method_test_implementation(self, test_signature):
        # TODO
        return ""

    # Main code
    def run_codeloop(self):
        print("starting codeloop")
        command_and_options_spec = self.get_commands_and_options_spec()

        methods_signatures_list = self.get_methods_signatures()

        for method_signature_payload in methods_signatures_list:
            method_implementation = self.write_method_body_implementation(
                method_signature_payload
            )
            test_signatures = self.write_method_test_signatures(method_implementation)

            all_method_tests = []
            for test_sig in test_signatures:
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
                messages=messages,
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
                        r"```(?:[a-zA-Z0-9_\-]+)?\n?(.*)\n?```",
                        response_text,
                        re.DOTALL,
                    )
                else:
                    code_blocks = re.findall(
                        r"```\n?(.*)\n?```", response_text, re.DOTALL
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
                        print(f"Could not parse JSON from code block: {code_block}")
                        raise CodeBlockError(
                            f"Could not parse JSON from code block: {code_block}"
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
