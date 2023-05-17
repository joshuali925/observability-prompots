from langchain.llms import HuggingFaceHub
from langchain.embeddings import HuggingFaceHubEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import VectorDBQA
from langchain.model_laboratory import ModelLaboratory
from langchain.prompts import PromptTemplate
__import__('dotenv').load_dotenv()


template = """Question: {question}

Answer: Let's think step by step."""
prompt = PromptTemplate(template=template, input_variables=["question"])

embeddings = HuggingFaceHubEmbeddings()

flan_ul2 = HuggingFaceHub(repo_id="google/flan-ul2", model_kwargs={"temperature":0.1, "max_new_tokens":200})
flan_t5 = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.1, "max_new_tokens":200})

lab = ModelLaboratory.from_llms([flan_ul2, flan_t5], prompt=prompt)

lab.compare("what is 3*2*3?")
