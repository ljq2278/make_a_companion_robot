"""Tool for asking human input."""

from typing import Callable, Optional
from langchain.llms.base import LLM
from pydantic import Field

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.tools.base import BaseTool
from memory.buffer import ConversationBufferMemory
# from langchain.schema.messages import get_buffer_string

# def _print_func(text: str) -> None:
#     print("\n")
#     print(text)
#

class AskSelfRun(BaseTool):
    """Tool that adds the capability to ask user for input."""

    name = "askSelf"
    description = (
        "Useful for when you want to know something about yourself, "
        "input should be what you want to know about yourself."
    )

    # prompt_func: Callable[[str], None] = Field(default_factory=lambda: _print_func)
    llm: LLM = None
    memory:  ConversationBufferMemory = None
    def _run(
            self,
            query: str,
            run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the Human input tool."""
        # self.prompt_func(query)
        history = self.memory.buffer
        return self.llm.predict(history+"\n\n"+query)
        # return self.preset

    async def _arun(
            self,
            query: str,
            run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Use the Human tool asynchronously."""
        raise NotImplementedError("Human tool does not support async")
