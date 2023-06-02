from langchain import LLMChain, OpenAI
from langchain.agents import ZeroShotAgent, AgentExecutor
from langchain.chat_models import ChatAnthropic
from agent_tools import create_tools
from langchain.cache import SQLiteCache
from langchain.chains.router import MultiPromptChain
from base_llm import BaseModel

from base_llm import BaseModel


llm_cache = SQLiteCache(database_path=".langchain.db")


tools = create_tools()
prefix = """For any questions related to fetching response times or latencies of services, 
steps the below steps in order and for each step use the output of previous step as input to the next one:

1. Use the OTEL Architecture context to understand the services
2. Generate the required PPL Query
3. Execute the required PPL Query
4. Sumarize the result and put it out as a thought

You have access to the following tools:"""

prompt = ZeroShotAgent.create_prompt(tools, prefix=prefix)

basemodel = BaseModel(model_name="openai")
llm = basemodel.get_model()

llm_chain = LLMChain(llm=BaseModel().get_model(), prompt=prompt)
agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools, verbose=True)
agent_chain = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True)

agent_chain.run("What is the current response time of the product catalog service?")

