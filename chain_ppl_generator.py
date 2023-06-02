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

Find the emails in index 'accounts' where firstname is 'Hattie' or lastname is 'Frank'. email field is 'email'
source=`accounts` | where `firstname` = 'Hattie' or `lastname` = 'frank' | fields `email`

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

What is the average, minimum, maximum age in 'accounts' index?
source=`accounts` | stats avg(`age`), min(`age`), max(`age`)

Show all states sorted by average balance. balance field is 'balance', states field is 'state', index is 'accounts'
source=`accounts` | stats avg(`balance`) as avg_balance by `state` | sort avg_balance

What is the average price of products ordered in the last 7 days? price field is 'taxful_total_price', ordered date field is 'order_date', index is 'ecommerce'
source=`ecommerce` | where `order_date` < DATE_SUB(NOW(), INTERVAL 7 DAY) | stats avg(`taxful_total_price`) as avg_price

What is the average price of products ordered in the last 24 hours by every 2 hours? price field is 'taxful_total_price', ordered date field is 'order_date', index is 'ecommerce'
source=`ecommerce` | where `order_date` < DATE_SUB(NOW(), INTERVAL 24 HOUR) | stats avg(`taxful_total_price`) as avg_price by span(`order_date`, 2h)

----------------

{format_instructions}

Question: {question}
""".strip()

response_schemas = [ResponseSchema(name="query", description="This a PPL query")]
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
format_instructions = output_parser.get_format_instructions()

prompt = ChatPromptTemplate(
    messages=[
        SystemMessagePromptTemplate.from_template(system_template),
        HumanMessagePromptTemplate.from_template("{question}"),
    ],
    input_variables=["question"],
    partial_variables={"format_instructions": format_instructions},
)

llm_chain = LLMChain(llm=BaseModel().get_model(), prompt=prompt)
llm_chain_output = llm_chain("How many requests are being processed by the payment service per second? field for timestamp is 'startTime', field for service is 'process.serviceName', value for payment service is 'payment', index is 'jaeger-span-*'")

output = output_parser.parse(llm_chain_output['text'])
print("❗output:")
print(output)
