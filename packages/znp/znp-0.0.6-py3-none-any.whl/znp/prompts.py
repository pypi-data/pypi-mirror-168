#!/usr/bin/env python3
import re
from promptx import (
    PromptX,
    PromptXCmdError,
    PromptXError,
    PromptXSelectError,
)


class InvalidCmdPrompt(Exception):
    """Exception raised when user has invalid command prompt"""

    def __init__(self, error, message="ERROR: prompt_cmd not recognized"):
        self.error = error
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message} "{self.error}"'


class InputError(Exception):
    """Exception fzf or dmenu prompt fails"""

    def __init__(self, error, message="ERROR: Could not get user input", prefix=""):
        self.error = error
        self.prefix = prefix
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.prefix}{self.message}{self.error}"


def zathura_prompt(pid_dict, prompt_cmd, prompt_args=None):
    """
    Prompt user to select their desired instance
    """
    # Create a list of options made up of the second value of
    # z.pid_dict. This looks like "123456: /path/to/file.pdf"
    options = []
    for val in pid_dict.values():
        options.append(val[1])
    # See if user wants to use custom prompt
    r = re.compile(r"(--prompt|-p\s)")
    prompt = None if r.findall(prompt_args) else "Use: "
    # Ask user about what instance to use
    if not prompt_args:
        prompt_args = "-l 20 -i" if prompt_cmd != "fzf" else ""
    try:
        p = PromptX(prompt_cmd=prompt_cmd, default_args=prompt_args)
        choice = p.ask(options=options, prompt=prompt)
    except (PromptXError, PromptXCmdError, PromptXSelectError) as err:
        print(err, sys.stderr)
        return None

    # Search for the chosen instance and return it's pid
    for key, val in pid_dict.items():
        if val[1] == choice:
            return key

    return None
