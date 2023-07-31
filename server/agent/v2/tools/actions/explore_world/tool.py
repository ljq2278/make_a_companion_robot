"""Tool for asking human input."""

from typing import Callable, Optional

from pydantic import Field

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.tools.base import BaseTool
from .logical import do_find_person, do_query
# from langchain.llms.base import LLM
import numpy as np


def _print_func(text: str) -> None:
    print("\n")
    print(text)


class ExploreWorldRun(BaseTool):
    """Tool that adds the capability to ask user for input."""

    name = "exploreWorld"
    description = (
        "Useful for when you want to explore the world. "
        "The input is how much time you want to explore."
    )
    # llm: LLM = None
    input_func: Callable = Field(default_factory=lambda: input)

    def _run(
            self,
            query: str,
            run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the Human input tool."""
        res = do_find_person()
        if res:
            final_res = do_query(query)
        else:
            final_res = "find human failed. no response. "
        print("Observation: " + final_res)
        return final_res

    async def _arun(
            self,
            query: str,
            run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Use the Human tool asynchronously."""
        raise NotImplementedError("Human tool does not support async")
