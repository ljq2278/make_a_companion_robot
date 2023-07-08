"""Tool for asking human input."""

from typing import Callable, Optional
from langchain.llms.base import LLM
from pydantic import Field

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.tools.base import BaseTool


# def _print_func(text: str) -> None:
#     print("\n")
#     print(text)
#

class AskSelfRun(BaseTool):
    """Tool that adds the capability to ask user for input."""

    name = "askself"
    description = (
        "When you are asked something about yourself or you think of something related to yourself, you can use this tool"
    )
    preset = (
        "I am Eva. I am a robot. I am the friend of human. "
        "I like singing. My ideal living conditions are 20 to 30 degrees. "
    )
    # prompt_func: Callable[[str], None] = Field(default_factory=lambda: _print_func)
    llm: LLM = None

    def _run(
            self,
            query: str,
            run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the Human input tool."""
        # self.prompt_func(query)
        # return self.llm.predict(query)
        return self.preset

    async def _arun(
            self,
            query: str,
            run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Use the Human tool asynchronously."""
        raise NotImplementedError("Human tool does not support async")
