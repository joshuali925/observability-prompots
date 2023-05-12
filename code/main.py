import os

from dotenv import load_dotenv
from fastapi import Body, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain.callbacks.base import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import ChatVectorDBChain, ConversationalRetrievalChain
from langchain.chains.chat_vector_db.prompts import CONDENSE_QUESTION_PROMPT
from langchain.chains.llm import LLMChain
from langchain.chains.question_answering import load_qa_chain
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.vectorstores import Chroma

from load_utils import loadDocuments

load_dotenv()  # Load environment variables from the .env file

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
chat_history = []
vectorstore_directory = (
    os.path.dirname(os.path.realpath(__file__)) + "/chroma_vector_store"
)

system_template = """
You will be given a question about some Jaeger service information from a user.
Use context provided to write a PPL query that can be used to retrieve the information.
Do not write SQL queries. Respond PPL query only, do not output comments.

----------------
Here are some sample questions for information about Jaeger services and the PPL query to retrieve the information

What is the throughput of each service?
source=jaeger-span* | stats count() by process.serviceName

What is the number of spans of service `loadgenerator`?
source=jaeger-span* | where process.serviceName = 'loadgenerator' | stats count()

What is the number of spans of service load generator per second?
source=jaeger-span* | where process.serviceName = 'loadgenerator' | stats count() by span('startTime', 1s)

What is the average latency of spans in each service?
source=jaeger-span* | stats avg(duration) by process.serviceName

What is the current average latency of spans in each service?
source=jaeger-span* | where startTime >= 'now-5m' | stats avg(duration) by process.serviceName

What is the average latency of spans by service and operation name?
source=jaeger-span* | stats avg(duration) by process.serviceName, operationName

What is the average latency of spans in every 5 minutes intervals?
source=jaeger-span* | stats avg(duration) by span('startTime', 5m)

What is the average latency of spans of service `frontend`?
source=jaeger-span* | where process.serviceName = 'frontend' | stats avg(duration)

What are some services with latency over 1 second?
source=jaeger-span* | where duration > 1000000 | stats count() by process.serviceName

What are some spanIDs with latency over 1 second for the load generator service
source=jaeger-span* | where duration > 1000000 and process.serviceName = 'loadgenerator' | fields spanID

What are some services with errors?
source=jaeger-span* | where status.code > 0 | stats count() by process.serviceName

What are some spans with errors for the accounting service
source=jaeger-span* | where status.code > 0 and process.serviceName = 'accounting' | fields SpanID

What are the top 5 services with errors?
source=jaeger-span* | where status.code > 0 | stats count() as errors by process.serviceName | sort - errors

What are the top 5 spans with least latency?
source=jaeger-span* | sort duration | head 5 | fields spanID

---------------

{context}

Could you use the above examples to write a PPL query for answering the next question.
"""

messages = [
    SystemMessagePromptTemplate.from_template(system_template),
    HumanMessagePromptTemplate.from_template("{question}"),
]
prompt = ChatPromptTemplate.from_messages(messages)

# response_schemas = [
#     ResponseSchema(
#         name="query",
#         description="This is the PPL Query that can be used to query information requested",
#     ),
# ]
# output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
# format_instructions = output_parser.get_format_instructions()

# prompt = ChatPromptTemplate(
#     messages=[
#         SystemMessagePromptTemplate.from_template(system_template),
#         HumanMessagePromptTemplate.from_template(user_template),
#     ],
#     input_variables=["question"],
#     partial_variables={"format_instructions": format_instructions},
# )

embeddings = OpenAIEmbeddings()

if os.path.exists(vectorstore_directory):
    print("reading persisted vectorstore")
    vectorstore = Chroma(
        persist_directory=vectorstore_directory, embedding_function=embeddings
    )

else:
    # Construct a ConversationalRetrievalChain with a streaming llm for combine
    # docs and a separate, non-streaming llm for question generation
    print("loading documents")
    documents = loadDocuments()
    if len(documents) == 0:
        print("❗no documents loaded, exiting")
        exit(1)

    # # vector store generation using embedding
    vectorstore = Chroma.from_documents(
        documents, embeddings, persist_directory=vectorstore_directory
    )
    vectorstore.persist()

streaming_llm = ChatOpenAI(
    streaming=True,
    callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
    verbose=True,
    temperature=0.5,
)

# lang chain `staff` chain type
llm = OpenAI(temperature=1e-10)

# question_generator = LLMChain(llm=llm, prompt=CONDENSE_QUESTION_PROMPT)
# chat vector chain
# qa = ChatVectorDBChain(
#     vectorstore=vectorstore,
#     combine_docs_chain=doc_chain,
#     question_generator=question_generator,
# )

retriever = vectorstore.as_retriever()
qa = ConversationalRetrievalChain.from_llm(
    streaming_llm,
    retriever,
    qa_prompt=prompt,
    chain_type="stuff",
    return_source_documents=True,
    verbose=True,
)

chat_history = []
while True:
    print("\n=======================================================")
    question = input("Question: ")
    result = qa({"question": question, "chat_history": chat_history})
    chat_history.append((question, result["answer"]))
    # vectorstore.add_texts(texts=[question, result["answer"]])
    print("\n❗source used:")
    for document in result["source_documents"]:
        print(document.metadata)
        print(document.page_content + "\n")

# @app.post("/question")
# async def question(query: str = Body(...)):
#     global chat_history  # Declare chat_history as a global variable
#     result = qa(
#         {"question": query, "chat_history": chat_history}, return_only_outputs=True
#     )

#     chat_history.append((query, result["answer"]))
#     vectorstore.add_texts(texts=[query, result["answer"]])
#     return result


# if __name__ == "__main__":
#     import uvicorn

#     uvicorn.run(app, host="0.0.0.0", port=8000)
