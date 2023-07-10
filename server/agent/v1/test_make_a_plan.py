from agents.mrkl.base import ZeroShotAgent, MRKLChain
from llm.llama import get_llama_llm
from tools.ddg_search.tool import DuckDuckGoSearchRun
from tools.human.tool import HumanInputRun
from tools.askself.tool import AskSelfRun
from tools.response_to_env.tool import ResponseToEnv
from memory.buffer import ConversationBufferMemory
from agents.mrkl.prompt_with_example import FORMAT_INSTRUCTIONS, PREFIX, SUFFIX
from langchain import LLMChain
import numpy as np

# from langchain.agents import load_tools
nm = 'Eva'
save_period = 10
memory = ConversationBufferMemory(memory_key="chat_history", ai_prefix=nm + "(me)")
memory.load_from_file('saved')

llm = get_llama_llm()
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
# agent_obj = ZeroShotAgent.from_llm_and_tools(
#     llm, tools, callback_manager=None, verbose=True,
# )
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
    memory=memory
)
while True:
    # chat with env, should use interruption mode
    if np.random.random() > 0.1:
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
    memory.chat_memory.messages[-1].content = memory.ai_prefix + ': ' + memory.chat_memory.messages[-1].content
    if len(memory.chat_memory.messages) % save_period == 0:
        memory.save_to_file('saved', save_period)
