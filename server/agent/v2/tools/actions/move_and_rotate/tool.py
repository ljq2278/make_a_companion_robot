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
import re
import numpy as np


def get_longest_digit_string(s):
    match = re.match(r"\d+", s)
    if match:
        return match.group()
    else:
        return ""


def parse_param(query):
    for act in ["up", "back", "rotate"]:
        if act in query:
            param_lt = query.split("#")
            if len(param_lt) >= 2:
                dist = get_longest_digit_string(param_lt[1])
                if len(dist) > 0:
                    if act == "rotate":
                        dist = str(np.deg2rad(int(dist)))
                    return act + "#" + dist
    return None


class MoveAndRotateRun(BaseTool):
    """Tool that adds the capability to ask user for input."""

    name = "moveAndRotate"
    description = (
        "Useful for when you want to move or rotate your body. "
        "input is up#distance or back#distance or rotate#degree. "
        "for example: back#30cm. the other example: rotate#90"
    )
    # llm: LLM = None
    input_func: Callable = Field(default_factory=lambda: input)

    def _run(
            self,
            query: str,
            run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the Human input tool."""
        act_param = parse_param(query)
        if act_param is not None:
            response = send_message(CLIENT_ACTION_IP_PATH, data={'action': act_param})
            if response.text != "true":
                print("move or rotate failed!", act_param)
                return "something wrong when move or rotate! maybe you can try again"
            else:
                print("move or rotate success!", act_param)
                return "move or rotate success! your position and vision may changed! "
        else:
            print("input format error!")
            return "input format error! check you input format with the tool instruction"

    async def _arun(
            self,
            query: str,
            run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Use the Human tool asynchronously."""
        raise NotImplementedError("Human tool does not support async")
