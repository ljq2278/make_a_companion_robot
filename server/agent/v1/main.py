import time

from agents.mrkl.base import ZeroShotAgent, MRKLChain
# from llm.gpt4all_llm import get_vicuna13b_llm
from llm.llama import get_llama_llm
from tools.ddg_search.tool import DuckDuckGoSearchRun
from tools.human.tool import HumanInputRun
from tools.askself.tool import AskSelfRun
from tools.response_to_env.tool import ResponseToEnv
# from memory.buffer import ConversationBufferMemory
from memory.summary_buffer import ConversationSummaryBufferMemory
from agents.mrkl.prompt_with_example_v2 import FORMAT_INSTRUCTIONS, PREFIX, SUFFIX
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
memory = ConversationSummaryBufferMemory(memory_key="chat_history", ai_prefix=nm + "(me)", llm=llm, max_token_limit=conversation_size)
memory.load_from_file('saved')
current_ans = {
    "speech": "a man coming to me. ",
    "mood": "happy"
}
last_mtime_listen = os.path.getmtime(listen_file)


def parse_ans(ans):
    res = {"speech": ans, "mood": "normal"}
    tmp = ans.split(']')
    if len(tmp) < 2:
        return res
    tmp = ''.join(tmp[:-1])
    tmp = tmp.split('[')
    if len(tmp) < 2:
        return res
    res["speech"] = ''.join(tmp[:-1])
    res["mood"] = tmp[-1]
    return res


def get_human_input_from_terminal():
    print('\nsay sth ... \n')
    ret = input()
    return ret


def get_human_input_from_file():
    global last_mtime_listen
    if os.path.getmtime(listen_file) != last_mtime_listen:
        f = open(listen_file, 'r', encoding='utf-8')
        res = '\n'.join(f.readlines())
        print("\nfrom listen file: ", res, "\n")
        last_mtime_listen = os.path.getmtime(listen_file)
        return res
    else:
        print("nothing listened, sleep\n")
        time.sleep(1)
        return ""


def post_memory_process():
    global current_ans, memory
    memory.chat_memory.messages[-2].content = memory.human_prefix + ': ' + memory.chat_memory.messages[-2].content
    current_ans = parse_ans(memory.chat_memory.messages[-1].content)
    memory.chat_memory.messages[-1].content = memory.ai_prefix + ': ' + memory.chat_memory.messages[-1].content
    print("\nconversation length: ", len(memory.chat_memory.messages), '\n')
    json.dump(current_ans, open('saved/current.txt', 'w', encoding='utf-8'))
    memory.save_to_file('saved')


if __name__ == '__main__':

    tools = [
        DuckDuckGoSearchRun(),
        # HumanInputRun(),
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
        # chat with env, should use interruption mode
        if np.random.random() > 1:
            memory.human_prefix = 'Environment'
            ipt = "a man coming to me. (information from environment)"
            while True:
                try:
                    output = agent_executor.run(input=ipt)
                    if output is not None and len(output) > 1:
                        break
                except Exception as e:
                    print(e)
            post_memory_process()
        # chat with human
        else:
            memory.human_prefix = 'Human'
            ipt = get_human_input_from_file()
            # ipt = get_human_input_from_terminal()
            if ipt == "":
                continue
            else:
                while True:
                    try:
                        output = agent_executor.run(input=ipt)
                        if output is not None and len(output) > 1:
                            break
                    except Exception as e:
                        print(e)
                post_memory_process()
