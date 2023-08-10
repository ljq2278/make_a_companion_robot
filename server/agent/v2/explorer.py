import time
import requests
from agents.mrkl.base import ZeroShotAgent, MRKLChain
# from llm.gpt4all_llm import get_vicuna13b_llm
from llm.llama import get_llama_llm
from tools.ddg_search.tool import DuckDuckGoSearchRun
from server_utils.others import parse_txt_and_mood, wait_for_human_response
from tools.actions.async_tasks.explore_world.tool import ExploreWorldRun
from tools.actions.async_tasks.find_obj.tool import FindObjRun
from tools.actions.async_tasks.go_charge.tool import GoChargeRun
from tools.actions.async_tasks.find_person_chat.tool import FindPersonRun
from tools.query_self.tool import AskSelfRun
from server_utils.path import CLIENT_ACTION_IP_PATH
from server_utils.others import get_nl_states
# from memory.buffer import ConversationBufferMemory
# from memory.summary_buffer import ConversationSummaryBufferMemory
from langchain.memory.summary_buffer import ConversationSummaryBufferMemory
from agents.mrkl.prompt import FORMAT_INSTRUCTIONS, PREFIX, SUFFIX
from langchain import LLMChain
import numpy as np
import json
import os

# from langchain.agents import load_tools

# max_iterations = 20

llm = get_llama_llm()
nm = 'Eva'
conversation_size = 256
memory = ConversationSummaryBufferMemory(memory_key="chat_history", ai_prefix=nm + "(me)", human_prefix="Environment", llm=llm, max_token_limit=conversation_size)

if __name__ == '__main__':

    tools = [
        DuckDuckGoSearchRun(),
        AskSelfRun(memory=memory, llm=llm),
        FindPersonRun(),
        FindObjRun(),
        # GoChargeRun(),
        ExploreWorldRun()

    ]
    prompt = ZeroShotAgent.create_prompt(
        tools,
        prefix=PREFIX,
        suffix=SUFFIX,
        format_instructions=FORMAT_INSTRUCTIONS,
        input_variables=["input", "chat_history", "agent_scratchpad"],
    )
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    agent_obj = ZeroShotAgent(
        llm_chain=llm_chain,
        tools=tools,
        callback_manager=None,
        # verbose=True,
    )
    agent_executor = MRKLChain.from_agent_and_tools(
        agent=agent_obj,
        tools=tools,
        # verbose=True,
        memory=memory,
        # max_iterations=max_iterations
    )
    while True:
        # time.sleep(0.5)
        states = get_nl_states()
        # memory.human_prefix = 'Environment'
        ipt = "there is some information from sensors. "
        ipt += json.dumps(states, ensure_ascii=False)
        print("inputs: ", ipt)
        while True:
            try:
                output = agent_executor.run(input=ipt)
                if output is not None and len(output) > 1:
                    break
            except Exception as e:
                print(e)
        txt_mood = parse_txt_and_mood(output)
        response = requests.post(CLIENT_ACTION_IP_PATH, data={'action': "show_mood#" + txt_mood["mood"]})
        if response.text != "true":
            print("show mood failed in main!")
        response = requests.post(CLIENT_ACTION_IP_PATH, data={'action': "say#" + txt_mood["speech"]})
        if response.text != "true":
            print("talk failed in main!")
        wait_for_human_response()
