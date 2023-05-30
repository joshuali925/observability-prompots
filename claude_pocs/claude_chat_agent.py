from langchain.agents import Tool
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI, ChatAnthropic
from langchain.utilities import SerpAPIWrapper
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from agent_tools import create_tools

tools = create_tools()

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
llm = ChatAnthropic(temperature=0)
agent_chain = initialize_agent(
    tools,
    llm,
    agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    memory=memory,
)
print(
    agent_chain.run(
        "Can you execute the following PPL Query source=jaeger-span* | where process.serviceName = 'productcatalogservice'| stats avg(duration) as response_time?"
    )
)
