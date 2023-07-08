# flake8: noqa
PREFIX = """Answer the following questions as best you can. You have access to the following tools:"""
FORMAT_INSTRUCTIONS = """Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question"""
SUFFIX = """Begin!

Question: {input}
Thought:{agent_scratchpad}"""

# PREFIX = """Answer the following questions as best you can. You have access to the following tools:"""
# FORMAT_INSTRUCTIONS = """Use the following format:
#
# Question: the input question you must answer
# Thought: you should always think about what tool to use for the question
# Tool: the tool to take, should be one of [{tool_names}]
# Tool Input: the input to the tool
# Observation: the result from the tool
# ... (this Thought/Tool/Tool Input/Observation can repeat N times)
# Thought: I now know the final answer
# Final Answer: the final answer to the original input question"""
# SUFFIX = """
# example:
# Question: where is China?
# Thought: I must get the location of China
# Tool: duckduckgo
# Tool Input: location of China
# Observation: China is at the east of Asian
# Thought: I now know the final answer
# Final Answer: China is at the east of Asian
#
# Begin!
#
# Question: {input}
# Thought:{agent_scratchpad}"""


# PREFIX = """Answer the following questions as best you can. You have access to the following tools:"""
# FORMAT_INSTRUCTIONS = """Use the following format:
#
# Question: the input question you must answer
# Thought: you should always think about what to do
# Action: the action to take, should be one of [{tool_names}]
# Action Input: the input to the action
# Observation: the result of the action
# ... (this Thought/Action/Action Input/Observation can repeat N times)
# Thought: I now know the final answer
# Final Answer: the final answer to the original input question"""
# SUFFIX = """
# this is an example:
# Question: where is China?
# Thought: I must get the location of China
# Action: duckduckgo
# Action Input: location of China
# Observation: China is at the east of Asian
# Thought: I now know the final answer
# Final Answer: China is at the east of Asian
#
# Begin!
#
# Question: {input}
# Thought:{agent_scratchpad}"""