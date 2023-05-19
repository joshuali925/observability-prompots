from typing import Any, List, Mapping, Optional

from langchain import HuggingFaceHub, OpenAI
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chat_models import ChatAnthropic
from langchain.embeddings import LlamaCppEmbeddings
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.embeddings.huggingface_hub import HuggingFaceHubEmbeddings
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import LlamaCpp
from langchain.llms import HuggingFacePipeline
from langchain.llms.base import LLM
import requests
from transformers import (
    AutoModelForCausalLM,
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
    pipeline,
)

__import__("dotenv").load_dotenv()


class BaseModel:
    """
    Base Model class to init the llm model to be used by tools, agents, planners and executor
    NOTE: In future this can have multiple options to easily switch between LLM models/params
    """

    llm = None
    embeddings = None

    def __init__(self, model_name="webui"):
        if model_name == "openai":
            self.llm = OpenAI(temperature=0)
            self.embeddings = OpenAIEmbeddings()

        elif model_name == "flan":
            self.llm = HuggingFaceHub(
                repo_id="google/flan-ul2", model_kwargs={"temperature": 0.1}
            )
            self.embeddings = HuggingFaceHubEmbeddings()

        elif model_name == "claude":
            self.llm = ChatAnthropic(temperature=0.7)
            # https://www.sbert.net/docs/pretrained_models.html
            # self.embeddings = HuggingFaceHubEmbeddings(repo_id="sentence-transformers/gtr-t5-xxl")
            self.embeddings = HuggingFaceEmbeddings()

        elif model_name == "llamaCpp":
            model_path = "./models/ggml-model-q4_0.bin"
            callbacks = [StreamingStdOutCallbackHandler()]
            self.llm = LlamaCpp(
                model_path=model_path,
                n_ctx=5000,
                callbacks=callbacks,
                n_threads=8,
                n_gpu_layers=40,
                verbose=True,
            )
            self.embeddings = LlamaCppEmbeddings(model_path=model_path)

        elif model_name == "webui":
            self.llm = WebuiLLM()
            self.embeddings = HuggingFaceHubEmbeddings()

        elif model_name == "pipeline":
            model_id = "google/flan-t5-large"
            tokenizer = AutoTokenizer.from_pretrained(model_id)
            model = AutoModelForSeq2SeqLM.from_pretrained(model_id)
            self.llm = HuggingFacePipeline(
                pipeline=pipeline(
                    "text2text-generation",
                    model=model,
                    tokenizer=tokenizer,
                    max_length=1000,
                )
            )
            self.embeddings = HuggingFaceEmbeddings()

    def get_model(self):
        return self.llm

    def get_embeddings(self):
        return self.embeddings


outputs = [
    """
Here is a step-by-step process to answer the question:
Question: What is the average latency of Fraud Detection Service?
Thought: I need the index name that contains latency data
Action: Schema knowledge
Action Input: Latency data
""",
    """
Thought: I can now construct the PPL query to retrieve the average latency of the Fraud Detection Service.
Final Answer: source='jaeger-span-*' | where process.serviceName = 'frauddetection' | stats avg(duration)
""",
]


# https://github.com/ChobPT/oobaboogas-webui-langchain_agent/blob/0fb15464869ce59d9b48bae5415d6a573a03ac5f/script.py#L179
class WebuiLLM(LLM):
    @property
    def _llm_type(self) -> str:
        return "custom"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        print('❗stop:', stop)
        print("❗prompt is")
        print(prompt)
        print("===================== prompt end =======================")
        if len(outputs) > 0:
            print("reading output")
            return outputs.pop(0)
        else:
            print("no more outputs. exiting.")
            exit(0)

        response = requests.post(
            "http://localhost:5000/api/v1/generate",
            json={
                "prompt": prompt,
                "max_new_tokens": 200,
                "do_sample": True,
                "temperature": 0.7,
                "top_p": 0.1,
                "typical_p": 1,
                "repetition_penalty": 1.18,
                "top_k": 40,
                "min_length": 0,
                "no_repeat_ngram_size": 0,
                "num_beams": 1,
                "penalty_alpha": 0,
                "length_penalty": 1,
                "early_stopping": True,
                "seed": -1,
                "add_bos_token": True,
                "truncation_length": 2048,
                "ban_eos_token": False,
                "skip_special_tokens": False,
                "stopping_strings": stop,
            },
        )

        response.raise_for_status()

        return response.json()["results"][0]["text"].strip()

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {}
