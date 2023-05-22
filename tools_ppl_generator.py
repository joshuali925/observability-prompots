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
Here are some sample questions and the PPL query to retrieve the information.

Give me some documents in index 'accounts'
source=`accounts`

Give me 10 documents in index 'accounts'
source=`accounts` | head 10

Give me 5 oldest people in index 'accounts'
source=`accounts` | sort - age | head 5

Give me first names of 5 youngest people in index 'accounts'
source=`accounts` | sort age | head 5 | fields `firstname`

Give me some addresses in index 'accounts'. field for addresses is 'address'
source=`accounts` | fields `address`

Find the document in index 'accounts' where firstname is 'Hattie'
source=`accounts` | where `firstname` = 'Hattie'

Find the document in index 'accounts' where firstname is 'Hattie' or lastname is 'Frank'
source=`accounts` | where `firstname` = 'Hattie' or `lastname` = 'frank'

Find the document in index 'accounts' where firstname is not 'Hattie' and lastname is not 'Frank'
source=`accounts` | where `firstname` != 'Hattie' and `lastname` != 'frank'

Count the number of documents in index 'accounts'
source=`accounts` | stats count()

Count the number of people with firstname 'Amber' in index 'accounts'
source=`accounts` | where `firstname`='Amber' | stats count()

How many people are older than 33? index is 'accounts', age fields is 'age'
source=`accounts` | where `age` > 33 | stats count()

How many males and females in index 'accounts'? gender fields is 'gender'
source=`accounts` | stats count() by `gender`

What is the average age in 'accounts' index?
source=`accounts` | stats avg(`age`)

What is the minimum age in 'accounts' index?
source=`accounts` | stats min(`age`)

What is the maximum age in 'accounts' index?
source=`accounts` | stats max(`age`)

---------------

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

agent_chain.run(input="what is the average latency of Fraud Detection Service? field for latency is 'duration', field for service is 'process.serviceName', value for Fraud Detection Service is 'frauddetectionservice', index is 'jaeger-span-*'")
