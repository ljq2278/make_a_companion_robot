from agents.mrkl.base import ZeroShotAgent, MRKLChain
from llm.llama import get_llama_llm
from tools.ddg_search.tool import DuckDuckGoSearchRun
from tools.human.tool import HumanInputRun, get_input
from tools.askself.tool import AskSelfRun
from memory.buffer import ConversationBufferMemory
from agents.mrkl.prompt_with_example import FORMAT_INSTRUCTIONS, PREFIX, SUFFIX
from langchain import LLMChain

# from langchain.agents import load_tools
save_period = 10
llm = get_llama_llm()
# tmp = llm.predict("You are a robot named Eva and you are the friend of human. And you like singing and you like to live in the temperature of 20 to 30 degree centigrade. Your name is ")
tools = [
    DuckDuckGoSearchRun(),
    HumanInputRun(),
    # AskSelfRun()
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
    llm_chain=llm_chain, tools=tools, callback_manager=None, verbose=True,
)
memory = ConversationBufferMemory(memory_key="chat_history")
memory.load_from_file('saved')
agent_executor = MRKLChain.from_agent_and_tools(
    agent=agent_obj,
    tools=tools,
    verbose=True,
    memory=memory
)
while True:
    print('say sth ... \n')
    ipt = input()
    while True:
        try:
            output = agent_executor.run(input=ipt)
            if output is not None and len(output) > 1:
                break
        except Exception as e:
            print(e)
    if len(memory.chat_memory.messages) % save_period == 0:
        memory.save_to_file('saved', save_period)
