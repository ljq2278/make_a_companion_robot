"""Tool for the DuckDuckGo search API."""
import os.path
import time
import warnings
from typing import Any, Optional
from server.utils.path import VISION_ACTION_COMPLETE_FILE, VISION_ACTION_RESULT_FILE, VISION_ACTION_FILE
from pydantic import Field

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.tools.base import BaseTool
from langchain.utilities.duckduckgo_search import DuckDuckGoSearchAPIWrapper


class VisionTool(BaseTool):
    name = "vision"
    description = (
        "Useful for when you need to use vision function to interact with the world."
        "Input is the direction that you want to look at. It should be one of (around/left/right/ahead)."
    )

    action_complete_file = VISION_ACTION_COMPLETE_FILE
    vision_result_file = VISION_ACTION_RESULT_FILE
    action_file = VISION_ACTION_FILE

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
        try:
            os.remove(self.action_complete_file)
        except Exception as e:
            pass
        f = open(self.action_file, 'w', encoding='utf-8')
        if "around" in query:
            f.write("look_around")
        elif "left" in query:
            f.write("look_at_left")
        elif "right" in query:
            f.write("look_at_right")
        elif "ahead" in query or "front" in query:
            f.write("look_ahead")
        else:
            f.write("look_around")
        f.close()
        ret = "I can see " + self._get_objs()+". Should I get to some other places?"
        print(ret)
        return ret

    async def _arun(
            self,
            query: str,
            run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("DuckDuckGoSearch does not support async")
