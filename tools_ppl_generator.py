from langchain import LLMChain, PromptTemplate
from langchain.agents import AgentExecutor, Tool, ZeroShotAgent
from langchain.chat_models import ChatAnthropic, ChatOpenAI
from langchain.llms import Anthropic, OpenAI
from langchain.memory import ConversationBufferMemory, ReadOnlySharedMemory
from langchain.utilities import GoogleSearchAPIWrapper

from agent_tools import create_tools, otel_knowledge
from base_llm import BaseModel

__import__("dotenv").load_dotenv()


prefix = """
You will be given a question about some metrics from a user.
Use context provided to write a PPL query that can be used to retrieve the information.

----------------
Here are some sample questions and the PPL query to retrieve the information. Format:

a. Question
b. PPL query with sample schema
c. PPL query with placeholder variables

[index] is a placeholder for index name.
[field] is a placeholder for a field name.
[value] is a placeholder for a field value.

Examples:

a. What is the throughput of each service?
b. source=jaeger-span* | stats count() by process.serviceName
c. source=[index] | stats count() by [field]

a. What is the number of spans of service 'loadgenerator'?
b. source=jaeger-span* | where process.serviceName = 'loadgenerator' | stats count()
c. source=[index] | where [field] = '[value]' | stats count()

a. What is the number of spans of service load generator per second?
b. source=jaeger-span* | where process.serviceName = 'loadgenerator' | stats count() by span('startTime', 1s)
c. source=[index] | where [field] = '[value]' | stats count() by span('[field]', 1s)

a. What is the average latency of spans in each service?
b. source=jaeger-span* | stats avg(duration) by process.serviceName
c. source=[index] | stats avg([field]) by [field]

a. What is the current average latency of spans in each service?
b. source=jaeger-span* | where startTime >= 'now-5m' | stats avg(duration) by process.serviceName
c. source=[index] | where [field] >= 'now-5m' | stats avg([field]) by [field]

a. What is the average latency of spans by service and operation name?
b. source=jaeger-span* | stats avg(duration) by process.serviceName, operationName
c. source=[index] | stats avg([field]) by [field], [field]

a. What is the average latency of spans in every 5 minutes intervals?
b. source=jaeger-span* | stats avg(duration) by span('startTime', 5m)
c. source=[index] | stats avg([field]) by span('[field]', 5m)

a. What is the average latency of spans of service `frontend`?
b. source=jaeger-span* | where process.serviceName = 'frontend' | stats avg(duration)
c. source=[index] | where [field] = '[value]' | stats avg([field])

a. What are some services with latency over 1 second?
b. source=jaeger-span* | where duration > 1000000 | stats count() by process.serviceName
c. source=[index] | where [field] > 1000000 | stats count() by [field]

a. What are some spanIDs with latency over 1 second for the load generator service
b. source=jaeger-span* | where duration > 1000000 and process.serviceName = 'loadgenerator' | fields spanID
c. source=[index] | where [field] > 1000000 and [field] = '[value]' | fields [field]

a. What are some services with errors?
b. source=jaeger-span* | where status.code > 0 | stats count() by process.serviceName
c. source=[index] | where [field] > 0 | stats count() by [field]

a. What are some spans with errors for the accounting service
b. source=jaeger-span* | where status.code > 0 and process.serviceName = 'accounting' | fields SpanID
c. source=[index] | where [field] > 0 and [field] = '[value]' | fields [field]

a. What are the top 5 services with errors?
b. source=jaeger-span* | where status.code > 0 | stats count() as errors by process.serviceName | sort - errors
c. source=[index] | where [field] > 0 | stats count() as errors by [field] | sort - errors

a. What are the top 5 spans with least latency?
b. source=jaeger-span* | sort duration | head 5 | fields spanID
c. source=[index] | sort [field] | head 5 | fields [field]

---------------

Before you write the query, use tools to replace placeholder values. A tool can only be used once
You have access to the following tools:
"""


suffix = """
Begin!

{chat_history}
Question: {input}
{agent_scratchpad}"""

tools = create_tools()
memory = ConversationBufferMemory(memory_key="chat_history")

prompt = ZeroShotAgent.create_prompt(
    tools,
    prefix=prefix,
    # suffix=suffix,
    # input_variables=["input", "chat_history", "agent_scratchpad"],
)

llm_chain = LLMChain(llm=BaseModel().get_model(), prompt=prompt)
agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools, verbose=True)
agent_chain = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=2,
    early_stopping_method="generate",
    memory=memory,
)

agent_chain.run(input="what is the average latency of Fraud Detection Service?")
