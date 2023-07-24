"""Tool for the DuckDuckGo search API."""
import os.path
import time
import warnings
from typing import Any, Optional
from server.utils.path import MOVE_ACTION_COMPLETE_FILE,  MOVE_ACTION_FILE
from pydantic import Field

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.tools.base import BaseTool


class MoveTool(BaseTool):
    name = "move"
    description = (
        "Useful for when you want to move to interact with the world."
        "Useful for when you want to find somthing different."
        "Input is the (Direction,Distance) that you want move. "
        "Direction should be one of (forward/backward/left/right). "
        "Distance should be one of (0cm/1cm/3cm/6cm). "
        "for example: ```action: move; action input: forward, 3cm"
    )

    action_complete_file = MOVE_ACTION_COMPLETE_FILE
    # vision_result_file = VISION_RESULT_FILE
    action_file = MOVE_ACTION_FILE

    def _get_result(self):
        while not os.path.exists(self.action_complete_file):
            time.sleep(0.2)
        os.remove(self.action_complete_file)
        return "I get to a new place. I should see what is the difference in the new place. "

    def _get_dest(self,query):
        if "6" in query:
            return "6"
        elif "3" in query:
            return "3"
        elif "1" in query:
            return "1"
        else:
            return "0"
    def _run(
            self,
            query: str,
            run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool."""
        try:
            os.remove(self.action_complete_file)
        except Exception as e:
            pass
        f = open(self.action_file, 'w', encoding='utf-8')
        if "forward" in query:
            dist = self._get_dest(query)
            f.write("forward_"+dist)
        elif "backward" in query:
            dist = self._get_dest(query)
            f.write("backward_" + dist)
        elif "left" in query:
            dist = self._get_dest(query)
            f.write("left_" + dist)
        elif "right" in query:
            dist = self._get_dest(query)
            f.write("right_" + dist)
        else:
            f.write("forward_0")
        f.close()
        ret = self._get_result()
        print(ret)
        return ret

    async def _arun(
            self,
            query: str,
            run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("DuckDuckGoSearch does not support async")
