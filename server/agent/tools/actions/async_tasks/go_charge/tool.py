"""Tool for asking human input."""

from typing import Callable, Optional
import requests
from pydantic import Field

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.tools.base import BaseTool
from server_utils.others import get_async_task_return, task_priorities


class GoChargeRun(BaseTool):
    """Tool that adds the capability to ask user for input."""

    name = "goCharge"
    description = (
            "Useful for when you want to charge yourself. Using this tool your current "
            + " or ".join([v1 for v1, v2 in sorted([(k, v) for k, v in task_priorities.items()], key=lambda x: x[1]) if v2 < task_priorities["goCharge"]]) +
            " task will be interrupted. "
            "input is the charge time you want to spend. "
    )
    # llm: LLM = None
    input_func: Callable = Field(default_factory=lambda: input)

    def _run(
            self,
            query: str,
            run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the Human input tool."""
        return get_async_task_return(self.name, query)

    async def _arun(
            self,
            query: str,
            run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Use the Human tool asynchronously."""
        raise NotImplementedError("Human tool does not support async")
