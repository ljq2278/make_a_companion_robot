"""Tool for the DuckDuckGo search API."""
import os.path
import time
import json
import re
from typing import Any, Optional
from server.utils.path import ACTION_RESULT_FILE, ACTION_FILE

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.tools.base import BaseTool


class RotateTool(BaseTool):
    name = "rotate"
    description = (
        "Useful for when you want to change your move or vision base direction."
        "Useful for when you want to find somthing different."
        "Input is the (Direction,Angle) that you want rotate. "
        "Direction should be one of (left/right). "
        "Angle should be from 0 to 180. "
        "for example: ```action: rotate; action input: left, 90```"
    )

    action_result_file = ACTION_RESULT_FILE
    # vision_result_file = VISION_RESULT_FILE
    action_file = ACTION_FILE
    pattern = r'\d+(\.\d+)?'
    def _get_act_from_query(self, query):
        direct = "left"
        if "right" in query:
            direct = "right"
        angle = "0"
        match = re.search(self.pattern, query)
        if match:
            angle = float(match.group())
        return {"action": "rotate", "direct": direct, "angle": str(angle)}

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
