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

# from langchain.agents import load_tools

llm = get_llama_llm()

nm = 'Eva'
max_iterations = 20
conversation_size = 256
memory = ConversationSummaryBufferMemory(memory_key="chat_history", ai_prefix=nm + "(me)", llm=llm, max_token_limit=conversation_size)
memory.load_from_file('saved')


tools = [
    DuckDuckGoSearchRun(),
    HumanInputRun(),
    AskSelfRun(memory=memory, llm=llm),
    ResponseToEnv(memory=memory, llm=llm)
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
    max_iterations=max_iterations
)
current_ans = {
    "speech": "a man coming to me. ",
    "mood": "happy"
}


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
    # chat with human
    else:
        memory.human_prefix = 'Human'
        print('\nsay sth ... \n')
        ipt = input()
        while True:
            try:
                output = agent_executor.run(input=ipt)
                if output is not None and len(output) > 1:
                    break
            except Exception as e:
                print(e)
    memory.chat_memory.messages[-2].content = memory.human_prefix + ': ' + memory.chat_memory.messages[-2].content
    current_ans = parse_ans(memory.chat_memory.messages[-1].content)
    memory.chat_memory.messages[-1].content = memory.ai_prefix + ': ' + memory.chat_memory.messages[-1].content
    print("\nconversation length: ", len(memory.chat_memory.messages), '\n')
    json.dump(current_ans, open('saved/current.txt', 'w', encoding='utf-8'))
    memory.save_to_file('saved')
