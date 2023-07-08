
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
if the Observation is "say to the questioner", that mean your Action Input is the Final Answer.
these are some examples: 

Question: where is China?
Thought: I must get the location of China
Action: duckduckgo
Action Input: location of China
Observation: China is at the east of Asian
Thought: I now know the final answer
Final Answer: China is at the east of Asian

Question: what is your name?
Thought: I should ask myself to get my name
Action: askself
Action Input: what is my name
Observation: my name is John
Thought: I now know the final answer
Final Answer: my name is John


Question: Can you tell my some recipes?
Thought: I must know what kind of recipe the questioner want
Action: human
Action Input: What kind of recipe do you want?
Observation: say to the questioner
Final Answer: What kind of recipe do you want?

Begin!
{chat_history}
Question: {input}
Thought:{agent_scratchpad}"""


# Question: Can you tell my some recipes?
# Thought: I must know what kind of recipe the questioner want
# Action: human
# Action Input: What kind of recipe do you want?
# Observation: make a pizza
# Thought: I must know how to make a pizza
# Action: duckduckgo
# Action Input: how to make a pizza
# Observation: buy a pizza from supermarket and put it in the oven to bake about 15 minutes and then you can enjoy the pizza
# Thought: I now know the final answer
# Final Answer: buy a pizza from supermarket and put it in the oven to bake about 15 minutes and then you can enjoy the pizza