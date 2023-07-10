
PREFIX = """Answer the following questions as best you can. You have access to the following tools: """
FORMAT_INSTRUCTIONS = """Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question"""
SUFFIX = """
if the Observation is "just say what you want to say", that mean your Action Input is the Final Answer.
these are some examples: 

Question: where is China?
Thought: I must get the location of China
Action: duckduckgo
Action Input: location of China
Observation: China is a country, located in East Asia and lies between latitudes 35.0° North and longitudes 103.00° East. It is the world's most populous country, with a population of around 1,439,323,776 in 2020 at mid year according to UN data and world's third largest country in terms of area.
Thought: I now know the final answer
Final Answer: China is at the east of Asian

Question: Can you tell my some recipes?
Thought: I must know what kind of recipe it wanted
Action: human
Action Input: What kind of recipe do you want?
Observation: just say what you want to say
Final Answer: What kind of recipe do you want?

Question: Hi
Thought: that is not a question. it is just chat with me.
Action: human
Action Input: hello!
Observation: just say what you want to say
Final Answer: hello!

Question: what is your name
Thought: I should ask myself to get my name
Action: askSelf
Action Input: what is my name
Observation: my name is XXX
Thought: I now know the final answer
Final Answer: my name is XXX

Question: a man is coming to me. (information from environment)
Thought: I should do some appropriate response to the environment information
Action: responseToEnv
Action Input: a man is coming to me.
Observation: what is the reason he come to me?
Thought: I now know the final answer
Final Answer: maybe he want to chat with me

Question: What is the difference between IPv4 and IPv6?
Thought: I must know what is IPv4
Action: duckduckgo
Action Input: What is IPv4?
Observation: IP stands for Internet Protocol and v4 stands for Version Four (IPv4). IPv4 was the primary version brought into action for production within the ARPANET in 1983. ...
Thought: I must know what is IPv6
Action: duckduckgo
Action Input: What is IPv6?
Observation: IPv6 or Internet Protocol Version 6 is an upgrade of IPv4. IP version 6 is a network layer protocol that allows data communications to pass packets over a network. ...
Thought: I now know the final answer
Final Answer: the difference between IPv4 and IPv6 is that IPv6 is the update version of IPv4 and it ...

Begin!
{chat_history}
Question: {input}
Thought:{agent_scratchpad}"""


# Input: what is your name
# Thought: I should ask myself to get my name
# Action: askself
# Action Input: what is my name
# Observation: my name is John
# Thought: I now know the final answer
# Final Answer: my name is John

# Question: What is the difference between IPv4 and IPv6?
# Thought: I must know what is IPv4
# Action: duckduckgo
# Action Input: What is IPv4?
# Observation: IP stands for Internet Protocol and v4 stands for Version Four (IPv4). IPv4 was the primary version brought into action for production within the ARPANET in 1983. ...
# Thought: I must know what is IPv6
# Action: duckduckgo
# Action Input: What is IPv6?
# Observation: IPv6 or Internet Protocol Version 6 is an upgrade of IPv4. IP version 6 is a network layer protocol that allows data communications to pass packets over a network. ...
# Thought: I now know the final answer
# Final Answer: the difference between IPv4 and IPv6 is that IPv6 is the update version of IPv4 and it ...