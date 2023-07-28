"""Tool for the DuckDuckGo search API."""
import os.path
import time
import json
import warnings
from typing import Any, Optional
from server.server_utils.path import ACTION_RESULT_FILE, ACTION_FILE

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
        "Direction should be one of (forward/backward). "
        "Distance should be one of (1cm/2cm/3cm/4cm). "
        "for example: ```action: move; action input: forward, 1cm```"
    )

    action_result_file = ACTION_RESULT_FILE
    # vision_result_file = VISION_RESULT_FILE
    action_file = ACTION_FILE

    def _get_act_from_query(self, query):
        direct = "forward"
        if "backward" in query:
            direct = "backward"
        dist = "0"
        if "3" in query:
            dist = 3
        elif "2" in query:
            dist = 2
        elif "1" in query:
            dist = 1
        return {"action": "move", "direct": direct, "dist": dist}

    def _run(
            self,
            query: str,
            run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool."""
        last_modify_time = os.path.getmtime(self.action_result_file)
        act_obj = self._get_act_from_query(query)
        f = open(self.action_file, 'w', encoding='utf-8')
        f.write(json.dumps(act_obj, ensure_ascii=False))
        f.close()
        while os.path.getmtime(self.action_result_file) == last_modify_time:
            time.sleep(0.5)
        f = open(self.action_result_file, 'r', encoding='utf-8')
        ret = f.read()
        f.close()
        print(ret)
        return ret

    async def _arun(
            self,
            query: str,
            run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("DuckDuckGoSearch does not support async")
