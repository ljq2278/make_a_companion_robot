"""Tool for asking human input."""

from typing import Callable, Optional
import requests
from pydantic import Field

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.tools.base import BaseTool
from server_utils.others import get_async_task_info, task_priorities
from server_utils.path import CLIENT_ACTION_IP_PATH


class FindObjRun(BaseTool):
    """Tool that adds the capability to ask user for input."""

    name = "findObj"
    description = (
            "Useful for when you want to find some objects. Using this tool your current "
            + " or ".join([v1 for v1, v2 in sorted([(k, v) for k, v in task_priorities.items()], key=lambda x: x[1]) if v2 < task_priorities["findObj"]]) +
            " task will be interrupted. "
            "input is the object you want to search. "
    )
    # llm: LLM = None
    input_func: Callable = Field(default_factory=lambda: input)

    def _run(
            self,
            query: str,
            run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the Human input tool."""
        task_nm, task_state, task_res = get_async_task_info()
        if task_state == "on doing" and task_priorities[task_nm] >= task_priorities["findObj"]:
            return task_nm + " is still on doing, current task can not be started. "
        else:
            response = requests.post(CLIENT_ACTION_IP_PATH, data={'action': "findObj#" + query})
            if response.status_code == 200:
                return "start searching for %s, result can be checked later in the information from sensors. " % query
            else:
                return "something wrong with task startup, try it later. "

    async def _arun(
            self,
            query: str,
            run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Use the Human tool asynchronously."""
        raise NotImplementedError("Human tool does not support async")