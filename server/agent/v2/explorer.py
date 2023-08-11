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
from tools.actions.say_to_human.tool import SayToHumanRun
from tools.actions.move_and_rotate.tool import MoveAndRotateRun
from server_utils.path import CLIENT_ACTION_IP_PATH, DIALOG_SHOW_IP_PATH
from server_utils.others import States
# from memory.buffer import ConversationBufferMemory
# from memory.summary_buffer import ConversationSummaryBufferMemory
from langchain.memory.summary_buffer import ConversationSummaryBufferMemory
from agents.mrkl.prompt import FORMAT_INSTRUCTIONS, PREFIX, SUFFIX
from langchain import LLMChain
from server_utils.others import send_message
import json
import os

# from langchain.agents import load_tools

# max_iterations = 20

states = States()
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
        SayToHumanRun(),
        MoveAndRotateRun(),
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
        diff_states = states.get_critical_states()
        if len(diff_states) == 0:
            print("no state changed!\n")
            time.sleep(2)
            continue
        # memory.human_prefix = 'Environment'
        ipt = "there is some information from sensors. "
        ipt += json.dumps(diff_states, ensure_ascii=False)
        print("inputs: ", ipt)
        send_message(DIALOG_SHOW_IP_PATH, data={"content": "<Environment>: " + ipt + "\n"})
        while True:
            try:
                output = agent_executor.run(input=ipt)
                if output is not None and len(output) > 1:
                    break
            except Exception as e:
                print(e)
        txt_mood = parse_txt_and_mood(output)
        response = send_message(CLIENT_ACTION_IP_PATH, data={'action': "show_mood#" + txt_mood["mood"]})
        if response.text != "true":
            print("show mood failed in main!")
        response = send_message(CLIENT_ACTION_IP_PATH, data={'action': "say#" + txt_mood["speech"]})
        if response.text != "true":
            print("talk failed in main!")
        send_message(DIALOG_SHOW_IP_PATH, data={"content": "<Eva>: " + txt_mood["speech"] + "[" + txt_mood["mood"] + "]" + "\n"})
        wait_for_human_response()
