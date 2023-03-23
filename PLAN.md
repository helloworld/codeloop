command: codeloop generate

> What do you want the name of the package to be?
> base_encoder

> What are the set of requirements for the package?
> It should be able to base64 encode messages
> It should be able to base64 decode messages
> It should be able to ...

> Thinking...

> Here are the set of command and options for the CLI
> encode

    -base what base to use [default=64]

> decode

    -base what base to use [default=64]

> Is this okay?
> Yes

> Generating...

// Internal

- For each command:
  - Generate the list of helper methods (signature only) it needs to implement the command
    - We have unique req where each function can only be like 20 lines long
  - Generate the command implementation using the methods
  - For each method:
    - Write the method implementation
    - Write the tests (signature only) for the method
    - For each test
      - Write the test
    - For each test (loop until everything passes)
      - Run the test
      - Fix the code
        - Input:
          - existing code, test output
        - Output:
          - Returns new code

> Done!
