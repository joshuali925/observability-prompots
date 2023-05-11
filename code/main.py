from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from langchain.callbacks.base import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import ChatVectorDBChain, ConversationalRetrievalChain
from langchain.chains.chat_vector_db.prompts import CONDENSE_QUESTION_PROMPT
from langchain.chains.llm import LLMChain
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
import os
from dotenv import load_dotenv

#   chat prompt
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.vectorstores import Chroma


# Web Server.gitignore
from load_utils import loadDocuments

vectorstore_directory = (
    os.path.dirname(os.path.realpath(__file__)) + "/chroma_vector_store"
)

load_dotenv()  # Load environment variables from the .env file
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can customize this to allow specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# chat history list
chat_history = []

# default prompt
system_template = """Use the following pieces of context to answer the users question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
In any conversation only return the minimal response that answers exactly the requested question without adding any additional information or explanations.
When asked a question always try to match it with a Conversation Template - and answer that the scenario is described in the specific template

----------------
{context}"""
messages = [
    SystemMessagePromptTemplate.from_template(system_template),
    HumanMessagePromptTemplate.from_template("{question}"),
]
prompt = ChatPromptTemplate.from_messages(messages)

if os.path.exists(vectorstore_directory):
    print("reading persisted vectorstore")
    vectorstore = Chroma(
        persist_directory=vectorstore_directory, embedding_function=OpenAIEmbeddings()
    )

else:
    # Construct a ConversationalRetrievalChain with a streaming llm for combine
    # docs and a separate, non-streaming llm for question generation
    print("loading documents")
    documents = loadDocuments()
    if len(documents) == 0:
        print('❗documents:', documents)
        exit(1)

    # # vector store generation using embedding
    vectorstore = Chroma.from_documents(
        documents, OpenAIEmbeddings(), persist_directory=vectorstore_directory
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
question_generator = LLMChain(llm=llm, prompt=CONDENSE_QUESTION_PROMPT)

# chat vector chain
# qa = ChatVectorDBChain(
#     vectorstore=vectorstore,
#     combine_docs_chain=doc_chain,
#     question_generator=question_generator,
# )

retriever = vectorstore.as_retriever()
qa = ConversationalRetrievalChain.from_llm(
    streaming_llm, retriever, qa_prompt=prompt, chain_type="stuff"
)


chat_history = []
while True:
    question = input("question: ")
    result = qa(
        {"question": question, "chat_history": chat_history}, return_only_outputs=True
    )
    chat_history.append((question, result))
    vectorstore.add_texts(texts=[question, result])
    print(result)

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
