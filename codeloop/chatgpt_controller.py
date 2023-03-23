import openai
from rich.panel import Panel
from rich.pretty import Pretty
from codeloop.console import console
from rich.panel import Panel
import re
import json


DEBUG = True


class CodeBlockError(Exception):
    pass



class ChatGPTController:
    def __init__(self, package_name, requirements, relative_path):
        self.package_name = package_name
        self.requirements = requirements
        self.relative_path = relative_path
        self.system_messages = [
                {"role": "system", "content": "You are the distinguished principal staff tech lead engineer manager L10 at Google."},
                ]

    def get_commands_and_options_spec(self):
        messages = [{"content": 
    f"""Generate the CLI commands for a CLI tool that:
    {self.requirements}

    Return output as a JSON list inside a code block.
    e.g. [{{"command_name": "...",  [{{"option_name": "...", "option_description": "...}}]}}]
    """, 
    "role": "user"}]
        cli_spec_list= self._request_completion(self.system_messages + messages, extract_code_blocks=True, extract_jsons=True, include_lang=True, print_prompt=True)

        print("CLI command spec: ", cli_spec_list)
        return cli_spec_list

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
        self.get_commands_and_options_spec()

        methods_signatures_list = self.get_methods_signatures()

        for method_signature_payload in methods_signatures_list:
            method_implementation = self.write_method_body_implementation(method_signature_payload)
            test_signatures = self.write_method_test_signatures(method_implementation)
            
            all_method_tests = []
            for test_sig in test_signatures:
                method_test_implementation = self.write_method_test_implementation(test_sig)
                all_method_tests.append(method_test_implementation)
            
            has_failures= False 
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


    def _request_completion(self, messages, extract_code_blocks=False, extract_jsons=False, include_lang=False, model="gpt-3.5-turbo", print_prompt=False):
        if print_prompt:
            self._print_prompt(messages)

        ## TODO: Add retry logic
        def _request(
            messages, model, extract_code_blocks=False, extract_jsons=False, include_lang=False
        ):
            completion = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                max_tokens=3000,
            )

            response_text = completion.choices[0].message.content

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
                            print(f"Could not parse JSON from code block: {code_block}")
                            raise CodeBlockError(
                                f"Could not parse JSON from code block: {code_block}"
                            )

                    return jsons

                return code_blocks

            return [response_text]

        response = _request(messages, model, extract_code_blocks=extract_code_blocks, extract_jsons=extract_jsons, include_lang=include_lang)[0]

        if DEBUG:
            console.print(
                Panel.fit(
                    Pretty(response),
                    title="Response",
                    border_style="red",
                ),
            )

        return response
