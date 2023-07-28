"""Tool for the DuckDuckGo search API."""
import json
import os.path
import time
import warnings
from typing import Any, Optional
from server.server_utils.path import ACTION_RESULT_FILE, ACTION_FILE
from pydantic import Field

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.tools.base import BaseTool
from langchain.utilities.duckduckgo_search import DuckDuckGoSearchAPIWrapper


class LookTool(BaseTool):
    name = "look"
    description = (
        "Useful for when you need to use vision function to interact with the world."
        "Input is the direction that you want to look at. It should be one of (left/right/up)."
    )

    action_result_file = ACTION_RESULT_FILE
    action_file = ACTION_FILE

    def _get_act_from_query(self, query):
        direct = "up"
        if "left" in query:
            direct = "left"
        elif "right" in query:
            direct = "right"
        return {"action": "look", "direct": direct}

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
