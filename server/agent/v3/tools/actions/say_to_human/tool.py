"""Tool for asking human input."""

from typing import Callable, Optional
import requests
from pydantic import Field

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.tools.base import BaseTool
from server_utils.others import send_message
from server_utils.path import CLIENT_ACTION_IP_PATH


class SayToHumanRun(BaseTool):
    """Tool that adds the capability to ask user for input."""

    name = "sayToHuman"
    description = (
        "Useful for when you want to say something to human nearby. "
        "input is the words you want to say to the person. "
    )
    # llm: LLM = None
    input_func: Callable = Field(default_factory=lambda: input)

    def _run(
            self,
            query: str,
            run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the Human input tool."""
        response = send_message(CLIENT_ACTION_IP_PATH, data={'action': "say#" + query})
        if response.text != "true":
            print("talk to human failed!")
            return "something wrong with talking to human! maybe you can try again"
        else:
            print("talk to human success!")
            return "talk to human success! the human nearby may response later."

    async def _arun(
            self,
            query: str,
            run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Use the Human tool asynchronously."""
        raise NotImplementedError("Human tool does not support async")
