from dotenv import load_dotenv
from fastapi import Body, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import ConversationalRetrievalChain
from langchain.chains.chat_vector_db.prompts import CONDENSE_QUESTION_PROMPT
from langchain.chains.llm import LLMChain
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)

from base_llm import BaseModel
from ingest import create_vector_store


load_dotenv()  # Load environment variables from the .env file

system_template = """
You will be given a question and a schema for an index from a user.
Find all entities in the question, then correlate with schema to find the value of each entity.

----------------
Here are some sample questions and the PPL query to retrieve the information.

Question: Give me 5 oldest people in index 'accounts'
Schema:
- account_number
- balance
- firstname
- lastname
- age
- gender
- address
- employer
- email
- city
- state
Response: field for age is 'age'

Question: Give me some addresses in index 'accounts'
Schema:
- account_number
- balance
- firstname
- lastname
- age
- gender
- address
- employer
- email
- city
- state
Response: field for addresses is 'address'

Question: Find the document in index 'accounts' where firstname is 'Hattie'
Schema:
- account_number
- balance
- firstname
- lastname
- age
- gender
- address
- employer
- email
- city
- state
Response: field for firstname is 'firstname'

Question: Find the emails in index 'accounts' where firstname is 'Hattie' or lastname is 'Frank'
Schema:
- account_number
- balance
- firstname
- lastname
- age
- gender
- address
- employer
- email
- city
- state
Response: field for email is 'email'', field for firstname is 'firstname', field for lastname is 'lastname'

Question: How many requests are being processed by the payment service per second?
Schema:
- duration
- flags
- logs
- operationName
- parentSpanID
- process
- references
- spanID
- startTime
- startTimeMillis
- tag
- tags
- traceID
- process.serviceName
Response: field for timestamp is 'startTime', field for service is 'process.serviceName'

Question: How many males and females in index 'accounts'?
Schema:
- account_number
- balance
- firstname
- lastname
- age
- gender
- address
- employer
- email
- city
- state
Response: gender field is 'gender'

Question: Show all states sorted by average balance
Schema:
- account_number
- balance
- firstname
- lastname
- age
- gender
- address
- employer
- email
- city
- state
Response: states field is 'state', balance field is 'balance'

Question: What is the average price of products ordered in the last 7 days?
Schema:
- category
- currency
- customer_birth_date
- customer_first_name
- customer_full_name
- customer_gender
- customer_id
- customer_last_name
- customer_phone
- day_of_week
- day_of_week_i
- email
- event
- geoip
- manufacturer
- order_date
- order_id
- products
- sku
- taxful_total_price
- taxless_total_price
- total_quantity
- total_unique_products
- type
- user
Response: price field is 'taxful_total_price', ordered date field is 'order_date'

Question: What are the top 5 customers spent the most?
Schema:
- category
- currency
- customer_birth_date
- customer_first_name
- customer_full_name
- customer_gender
- customer_id
- customer_last_name
- customer_phone
- day_of_week
- day_of_week_i
- email
- event
- geoip
- manufacturer
- order_date
- order_id
- products
- sku
- taxful_total_price
- taxless_total_price
- total_quantity
- total_unique_products
- type
- user
Response: spending field is 'taxful_total_price', customer field is 'customer_id'

----------------

Question: {question}
""".strip()

prompt = ChatPromptTemplate(
    messages=[
        SystemMessagePromptTemplate.from_template(system_template),
        HumanMessagePromptTemplate.from_template("{question}"),
    ],
    input_variables=["question"],
)

llm_chain = LLMChain(llm=BaseModel().get_model(), prompt=prompt)
llm_chain_output = llm_chain(
    """
Question: What is the current response time of the product catalog service?
Schema:
- duration
- flags
- logs
- operationName
- parentSpanID
- process
- references
- spanID
- startTime
- startTimeMillis
- tag
- tags
- traceID
- process.serviceName
""".strip()
)

print(llm_chain_output["text"])
