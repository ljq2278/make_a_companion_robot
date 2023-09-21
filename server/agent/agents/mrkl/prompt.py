from .identities.dialog_game_player import identity, examples

PREFIX = """You are a character described below: 

%s

At the beginning of your response, show your mood. 
it should be one of (happy/sad/normal/angry/amazed/confused/scared). 
You have access to the following tools: """ % identity
FORMAT_INSTRUCTIONS = """
Use the following format:

Conversation_Input: the conversation input that you must make a response
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action. 
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: now I know the final response and the human response suggestions.
Final Response and Next Response Suggestions: [your mood]the final response to the conversation input and the suggested following human responses. 

"""

SUFFIX = """
these are some examples: 

%s

Begin!
{chat_history}
Conversation_Input: {input}
Thought:{agent_scratchpad}""" % examples

############################################################# chat

# Conversation_Input: a man is coming to me. (information from environment)
# Thought: I should do some appropriate response to the environment information
# Action: responseToEnv
# Action Input: a man is coming to me.
# Observation: what is the reason he come to me?
# Thought: I now know the final response
# Final Response: maybe he want to chat with me. [confused]

# Question: Can you tell my some recipes?
# Thought: I must know what kind of recipe it wanted
# Action: human
# Action Input: What kind of recipe do you want?
# Observation: just say what you want to say
# Final Answer: What kind of recipe do you want? [confused]
#
# Question: Hi
# Thought: that is not a question. it is just chat with me.
# Action: human
# Action Input: hello!
# Observation: just say what you want to say
# Final Answer: hello! [happy]
################################################################################
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
