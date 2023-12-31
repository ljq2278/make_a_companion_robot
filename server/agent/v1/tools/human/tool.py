"""Tool for asking human input."""

from typing import Callable, Optional

from pydantic import Field

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.tools.base import BaseTool


def _print_func(text: str) -> None:
    print("\n")
    print(text)

# def get_input() -> str:
#     print("Insert your text. Enter 'q' or press Ctrl-D (or Ctrl-Z on Windows) to end.")
#     contents = []
#     while True:
#         try:
#             line = input()
#         except EOFError:
#             break
#         if line == "q":
#             break
#         contents.append(line)
#     return "\n".join(contents)
class HumanInputRun(BaseTool):
    """Tool that adds the capability to ask user for input."""

    name = "chat"
    description = (
        "Useful for when you want to talk or ask to human or just chat "
        "The input is what you want to talk or ask."
    )
    prompt_func: Callable[[str], None] = Field(default_factory=lambda: _print_func)
    input_func: Callable = Field(default_factory=lambda: input)

    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the Human input tool."""
        self.prompt_func(query)
        # return self.input_func()
        return "the action input is the final response"

    async def _arun(
        self,
        query: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Use the Human tool asynchronously."""
        raise NotImplementedError("Human tool does not support async")
