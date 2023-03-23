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

    def get_commands_and_options(self):
        messages = [{"content": 
    f"""Generate the CLI commands for a CLI tool that:
    {self.requirements}

    Return output as a JSON list. 
    e.g. [{{"command_name": "...",  [{{"option_name": "...", "option_description": "...}}]}}]
    """, 
    "role": "user"}]
        cli_spec_list_raw_output = self._request_completion(self.system_messages + messages, extract_code_blocks=True, extract_jsons=True, include_lang=True)

        print("output: ", cli_spec_list_raw_output)

    def _print_prompt(messages):
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
            messages, extract_code_blocks=False, extract_jsons=False, include_lang=False
        ):
            completion = openai.ChatCompletion.create(
                model="gpt-4",
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

        response = _request(messages)[0]

        if DEBUG:
            console.print(
                Panel.fit(
                    Pretty(response),
                    title="Response",
                    border_style="red",
                ),
            )

        return response
