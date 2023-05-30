from langchain import LLMChain, PromptTemplate
from agent_tools import create_tools
from langchain.cache import SQLiteCache
from base_llm import BaseModel


llm_cache = SQLiteCache(database_path=".langchain.db")

tools = create_tools()

basemodel = BaseModel()
llm = basemodel.get_model()

nginx_logs = """
[`time`: `2023-05-02T13:15:22Z`, `request`: `POST /api/v1/order`, `status`: 201, `response_time`: 0.800, `bytes_sent`: 100, `upstream_response_time`: 0.600, `upstream_addr`: `10.0.0.6:8080`]
[`time`: `2023-05-02T13:16:22Z`, `request`: `POST /api/v1/order`, `status`: 201, `response_time`: 0.800, `bytes_sent`: 100, `upstream_response_time`: 0.600, `upstream_addr`: `10.0.0.6:8080`]
[`time`: `2023-05-02T13:17:22Z`, `request`: `POST /api/v1/order`, `status`: 201, `response_time`: 0.800, `bytes_sent`: 100, `upstream_response_time`: 0.600, `upstream_addr`: `10.0.0.6:8080`]
[`time`: `2023-05-02T13:18:22Z`, `request`: `POST /api/v1/order`, `status`: 201, `response_time`: 0.800, `bytes_sent`: 100, `upstream_response_time`: 0.600, `upstream_addr`: `10.0.0.6:8080`]
[`time`: `2023-05-02T13:19:22Z`, `request`: `POST /api/v1/order`, `status`: 201, `response_time`: 0.800, `bytes_sent`: 100, `upstream_response_time`: 0.600, `upstream_addr`: `10.0.0.6:8080`]
[`time`: `2023-05-02T13:20:22Z`, `request`: `POST /api/v1/order`, `status`: 201, `response_time`: 0.800, `bytes_sent`: 100, `upstream_response_time`: 0.600, `upstream_addr`: `10.0.0.6:8080`]
[`time`: `2023-05-02T13:21:23Z`, `request`: `POST /api/v1/order`, `status`: 201, `response_time`: 1.100, `bytes_sent`: 100, `upstream_response_time`: 0.900, `upstream_addr`: `10.0.0.6:8080`]
[`time`: `2023-05-02T13:22:23Z`, `request`: `POST /api/v1/order`, `status`: 201, `response_time`: 1.100, `bytes_sent`: 100, `upstream_response_time`: 0.900, `upstream_addr`: `10.0.0.6:8080`]
[`time`: `2023-05-02T13:23:23Z`, `request`: `POST /api/v1/order`, `status`: 201, `response_time`: 1.100, `bytes_sent`: 100, `upstream_response_time`: 0.900, `upstream_addr`: `10.0.0.6:8080`]
[`time`: `2023-05-02T13:24:23Z`, `request`: `POST /api/v1/order`, `status`: 201, `response_time`: 1.100, `bytes_sent`: 100, `upstream_response_time`: 0.900, `upstream_addr`: `10.0.0.6:8080`]
[`time`: `2023-05-02T13:25:23Z`, `request`: `POST /api/v1/order`, `status`: 201, `response_time`: 1.100, `bytes_sent`: 100, `upstream_response_time`: 0.900, `upstream_addr`: `10.0.0.6:8080`]
[`time`: `2023-05-02T13:26:23Z`, `request`: `POST /api/v1/order`, `status`: 201, `response_time`: 1.100, `bytes_sent`: 100, `upstream_response_time`: 0.900, `upstream_addr`: `10.0.0.6:8080`]
[`time`: `2023-05-02T13:27:24Z`, `request`: `POST /api/v1/order`, `status`: 201, `response_time`: 1.800, `bytes_sent`: 100, `upstream_response_time`: 1.200, `upstream_addr`: `10.0.0.6:8080`]
[`time`: `2023-05-02T13:28:24Z`, `request`: `POST /api/v1/order`, `status`: 201, `response_time`: 1.800, `bytes_sent`: 100, `upstream_response_time`: 1.200, `upstream_addr`: `10.0.0.6:8080`]
[`time`: `2023-05-02T13:29:24Z`, `request`: `POST /api/v1/order`, `status`: 201, `response_time`: 1.800, `bytes_sent`: 100, `upstream_response_time`: 1.200, `upstream_addr`: `10.0.0.6:8080`]
[`time`: `2023-05-02T13:30:24Z`, `request`: `POST /api/v1/order`, `status`: 201, `response_time`: 1.800, `bytes_sent`: 100, `upstream_response_time`: 1.200, `upstream_addr`: `10.0.0.6:8080`]
[`time`: `2023-05-02T13:31:24Z`, `request`: `POST /api/v1/order`, `status`: 201, `response_time`: 1.800, `bytes_sent`: 100, `upstream_response_time`: 1.200, `upstream_addr`: `10.0.0.6:8080`]
[`time`: `2023-05-02T13:32:25Z`, `request`: `POST /api/v1/order`, `status`: 201, `response_time`: 3.000, `bytes_sent`: 100, `upstream_response_time`: 2.500, `upstream_addr`: `10.0.0.6:8080`]
[`time`: `2023-05-02T13:33:25Z`, `request`: `POST /api/v1/order`, `status`: 201, `response_time`: 3.000, `bytes_sent`: 100, `upstream_response_time`: 2.500, `upstream_addr`: `10.0.0.6:8080`]
[`time`: `2023-05-02T13:34:25Z`, `request`: `POST /api/v1/order`, `status`: 201, `response_time`: 3.000, `bytes_sent`: 100, `upstream_response_time`: 2.500, `upstream_addr`: `10.0.0.6:8080`]
[`time`: `2023-05-02T13:35:25Z`, `request`: `POST /api/v1/order`, `status`: 201, `response_time`: 3.000, `bytes_sent`: 100, `upstream_response_time`: 2.500, `upstream_addr`: `10.0.0.6:8080`]
[`time`: `2023-05-02T13:36:25Z`, `request`: `POST /api/v1/order`, `status`: 201, `response_time`: 3.000, `bytes_sent`: 100, `upstream_response_time`: 2.500, `upstream_addr`: `10.0.0.6:8080`]
[`time`: `2023-05-02T13:37:25Z`, `request`: `POST /api/v1/order`, `status`: 201, `response_time`: 4.500, `bytes_sent`: 100, `upstream_response_time`: 3.800, `upstream_addr`: `10.0.0.6:8080`]
[`time`: `2023-05-02T13:38:25Z`, `request`: `POST /api/v1/order`, `status`: 201, `response_time`: 4.500, `bytes_sent`: 100, `upstream_response_time`: 3.800, `upstream_addr`: `10.0.0.6:8080`]
[`time`: `2023-05-02T13:39:25Z`, `request`: `POST /api/v1/order`, `status`: 201, `response_time`: 4.500, `bytes_sent`: 100, `upstream_response_time`: 3.800, `upstream_addr`: `10.0.0.6:8080`]
[`time`: `2023-05-02T13:40:25Z`, `request`: `POST /api/v1/order`, `status`: 201, `response_time`: 4.500, `bytes_sent`: 100, `upstream_response_time`: 3.800, `upstream_addr`: `10.0.0.6:8080`]
[`time`: `2023-05-02T13:15:26Z`, `request`: `POST /api/v1/order`, `status`: 201, `response_time`: 4.500, `bytes_sent`: 100, `upstream_response_time`: 3.800, `upstream_addr`: `10.0.0.6:8080`]
"""

prompt_template = (
    """
Use the following pieces of context to answer the users question. 
If you dont know the answer, just say that you dont know, dont try to make up an answer.
Your role is to help an engineer to solve system issues by looking at logs, traces and metrics.
Find issue in logs below, summarize the issue and provide next steps for the engineer to follow.

"""
    + nginx_logs
    + """
    {user_question}    
"""
)

# print(prompt_template)
prompt = PromptTemplate(input_variables=["user_question"], template=prompt_template)

llm_chain = LLMChain(llm=llm, prompt=prompt)

print(llm_chain("Can you find the issue in the nginx logs and provide next steps?"))
