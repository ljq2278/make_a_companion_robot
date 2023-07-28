import time
import requests
from agents.mrkl.base import ZeroShotAgent, MRKLChain
# from llm.gpt4all_llm import get_vicuna13b_llm
from llm.llama import get_llama_llm
from tools.ddg_search.tool import DuckDuckGoSearchRun
from server_utils.others import parse_txt_and_mood, wait_for_human_response
from tools.actions.find_person_and_chat.tool import InviteToChatRun
from tools.askself.tool import AskSelfRun
from server_utils.path import CLIENT_ACTION_IP_PATH
from states.state import get_states
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
listen_file = "../../auditory/record.txt"
llm = get_llama_llm()
nm = 'Eva'
conversation_size = 256
memory = ConversationSummaryBufferMemory(memory_key="chat_history", ai_prefix=nm + "(me)", human_prefix="Environment", llm=llm, max_token_limit=conversation_size)
# memory = ConversationSummaryBufferMemory(memory_key="chat_history", ai_prefix=nm + "(me)", llm=llm, max_token_limit=conversation_size)
# memory.load_from_file('saved')
# current_ans = {
#     "speech": "a man coming to me. ",
#     "mood": "happy"
# }
# last_mtime_listen = os.path.getmtime(listen_file)
#
#
# def parse_ans(ans):
#     res = {"speech": ans, "mood": "normal"}
#     tmp = ans.split(']')
#     if len(tmp) < 2:
#         return res
#     tmp = ''.join(tmp[:-1])
#     tmp = tmp.split('[')
#     if len(tmp) < 2:
#         return res
#     res["speech"] = ''.join(tmp[:-1])
#     res["mood"] = tmp[-1]
#     return res
#
#
# def post_memory_process():
#     global current_ans, memory
#     memory.chat_memory.messages[-2].content = memory.human_prefix + ': ' + memory.chat_memory.messages[-2].content
#     current_ans = parse_ans(memory.chat_memory.messages[-1].content)
#     memory.chat_memory.messages[-1].content = memory.ai_prefix + ': ' + memory.chat_memory.messages[-1].content
#     print("\nconversation length: ", len(memory.chat_memory.messages), '\n')
#     json.dump(current_ans, open('saved/current.txt', 'w', encoding='utf-8'))
#     memory.save_to_file('saved')


if __name__ == '__main__':

    tools = [
        DuckDuckGoSearchRun(),
        InviteToChatRun(),
        AskSelfRun(memory=memory, llm=llm),
        # ResponseToEnv(memory=memory, llm=llm)

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
        time.sleep(0.5)
        states = get_states()
        # memory.human_prefix = 'Environment'
        ipt = "there is some information from sensors. "
        ipt += json.dumps(states, ensure_ascii=False)
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
        # post_memory_process()
        # if states["human"] != "":
        #     memory.human_prefix = 'Human'
        #     # ipt = get_human_input_from_file()
        #     ipt = get_human_input_from_terminal()
        #     if ipt == "":
        #         continue
        #     else:
        #         while True:
        #             try:
        #                 output = agent_executor.run(input=ipt)
        #                 if output is not None and len(output) > 1:
        #                     break
        #             except Exception as e:
        #                 print(e)
        #         post_memory_process()
        # # chat with env, should use interruption mode
        # else:
        #     memory.human_prefix = 'Environment'
        #     ipt = "there is some information from environment. "
        #     ipt = ipt + "you can see: " + get_seeing()
        #     while True:
        #         try:
        #             output = agent_executor.run(input=ipt)
        #             if output is not None and len(output) > 1:
        #                 break
        #         except Exception as e:
        #             print(e)
        #     post_memory_process()
