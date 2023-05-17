from langchain import LLMChain, PromptTemplate
from langchain.agents import AgentExecutor, Tool, ZeroShotAgent
from langchain.chat_models import ChatAnthropic, ChatOpenAI
from langchain.llms import Anthropic, OpenAI
from langchain.memory import ConversationBufferMemory, ReadOnlySharedMemory
from langchain.utilities import GoogleSearchAPIWrapper

from agent_tools import create_tools, otel_knowledge

__import__("dotenv").load_dotenv()


prefix = """
You will be given a question about some metrics from a user.
Use context provided to write a PPL query that can be used to retrieve the information.

----------------
Here are some sample questions and the PPL query to retrieve the information.
[index] is a placeholder for index name, [field] is a placeholder for a field name, [value] is a placeholder for a field value.
Replace them with actual values from the question.

Query to get the throughput of each [field]?
source=[index] | stats count() by [field]

Query to get the number of spans of [field] [value]?
source=[index] | where [field] = '[value]' | stats count()

Query to get the number of spans of service load generator per second?
source=[index] | where [field] = '[value]' | stats count() by span('[field]', 1s)

Query to get the average latency of spans in each service?
source=[index] | stats avg([field]) by [field]

Query to get the current average latency of spans in each service?
source=[index] | where [field] >= 'now-5m' | stats avg([field]) by [field]

Query to get the average latency of spans by service and operation name?
source=[index] | stats avg([field]) by [field], [field]

Query to get the average latency of spans in every 5 minutes intervals?
source=[index] | stats avg([field]) by span('[field]', 5m)

Query to get the average latency of spans of service `frontend`?
source=[index] | where [field] = '[value]' | stats avg([field])

Query to get some services with latency over 1 second?
source=[index] | where [field] > 1000000 | stats count() by [field]

Query to get some spanIDs with latency over 1 second for the load generator service
source=[index] | where [field] > 1000000 and [field] = '[value]' | fields [field]

Query to get some services with errors?
source=[index] | where [field] > 0 | stats count() by [field]

Query to get some spans with errors for the accounting service
source=[index] | where [field] > 0 and [field] = '[value]' | fields [field]

Query to get the top 5 services with errors?
source=[index] | where [field] > 0 | stats count() as errors by [field] | sort - errors

Query to get the top 5 spans with least latency?
source=[index] | sort [field] | head 5 | fields [field]

---------------

Do not provide comments, only output the PPL query.

Before you write the query, use the OTEL Demo knowledge tool to first to get all the field names.

You have access to the following tools:"""


suffix = """Begin!"

{chat_history}
Question: {input}
{agent_scratchpad}"""

tools = create_tools()
memory = ConversationBufferMemory(memory_key="chat_history")

prompt = ZeroShotAgent.create_prompt(
    tools,
    prefix=prefix,
    suffix=suffix,
    input_variables=["input", "chat_history", "agent_scratchpad"],
)

llm_chain = LLMChain(llm=ChatAnthropic(temperature=0), prompt=prompt)
agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools, verbose=True)
agent_chain = AgentExecutor.from_agent_and_tools(
    agent=agent, tools=tools, verbose=True, memory=memory
)
agent_chain.run(input="what is the average latency of service load generator?")
