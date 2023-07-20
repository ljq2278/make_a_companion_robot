"""Tool for the DuckDuckGo search API."""
import os.path
import time
import warnings
from typing import Any, Optional
from server.utils.path import ACTION_COMPLETE_FILE, VISION_RESULT_FILE, ACTION_FILE
from pydantic import Field

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.tools.base import BaseTool
from langchain.utilities.duckduckgo_search import DuckDuckGoSearchAPIWrapper


class VisionTool(BaseTool):
    """Tool that adds the capability to query the DuckDuckGo search API."""

    name = "vision"
    description = (
        "Useful for when you need to use vision function to interact with the world"
        "Input should be one of the following params [look around, look at left, look at right, look ahead]."
    )
    api_wrapper: DuckDuckGoSearchAPIWrapper = Field(
        default_factory=DuckDuckGoSearchAPIWrapper
    )
    action_complete_file = ACTION_COMPLETE_FILE
    vision_result_file = VISION_RESULT_FILE
    action_file = ACTION_FILE

    def _get_objs(self):
        res = set()
        while not os.path.exists(self.action_complete_file):
            f_obj = open(self.vision_result_file, 'r', encoding='utf-8')
            for line in f_obj.readlines():
                res.add(line.strip())
            f_obj.close()
            time.sleep(0.2)
        os.remove(self.action_complete_file)
        return ",".join(list(res))

    def _run(
            self,
            query: str,
            run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool."""
        f = open(self.action_file, 'w', encoding='utf-8')
        if "look around" in query:
            f.write("look_around")
        elif "look at left" in query:
            f.write("look_at_left")
        elif "look at right" in query:
            f.write("look_at_right")
        elif "look ahead" in query:
            f.write("look_ahead")
        f.close()
        ret = self._get_objs()
        print(ret)
        return ret

    async def _arun(
            self,
            query: str,
            run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("DuckDuckGoSearch does not support async")
