from langchain import LLMChain, OpenAI
from langchain.agents import ZeroShotAgent, AgentExecutor
from agent_tools import create_tools
from langchain.cache import SQLiteCache
from langchain.chains.router import MultiPromptChain
from base_llm import BaseModel


llm_cache = SQLiteCache(database_path=".langchain.db")


tools = create_tools()
# CUSTOM_PREFIX = """Answer the following questions as best you can. You have access to the following tools:"""
# CUSTOM_FORMAT_INSTRUCTIONS = """Always use the following format:

# Question: the input question you must answer
# Thought: you should always think about what to do
# Action: the action to take, should be one of [{tool_names}]
# Action Input: the input to the action
# Observation: the result of the action
# ... (this Thought/Action/Action Input/Observation can repeat N times, Only repeat when you don't know the final answer)
# Think: Do I know the final answer?
# Thought: I now know the final answer or No, I don't know the final answer. Mention your next action.
# Final Answer: the final answer to the original input question"""
# CUSTOM_SUFFIX = """Begin!

# Question: {input}
# Thought:{agent_scratchpad}"""

prompt = ZeroShotAgent.create_prompt(
    tools,
    # prefix=CUSTOM_PREFIX,
    # format_instructions=CUSTOM_FORMAT_INSTRUCTIONS,
    # suffix=CUSTOM_SUFFIX,
)

print(prompt)

basemodel = BaseModel(model_name="claude")
llm = basemodel.get_model()

llm_chain = LLMChain(llm=llm, prompt=prompt)
agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools, verbose=True)
agent_chain = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True)

agent_chain.run(
    "Can you please execute this PPL Query: source=jaeger-span-2023-05-20 | where startTimeMillis >= '2023-05-01 07:00:00' and startTimeMillis <= '2023-06-01 06:59:59' | where duration > 100000 | stats count() by span(startTimeMillis, 1d)"
)

