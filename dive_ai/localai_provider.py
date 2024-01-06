from jupyter_ai_magics import BaseProvider, BaseEmbeddingsProvider
from langchain.llms import FakeListLLM
from langchain.embeddings import FakeEmbeddings


class LocalAIProvider(BaseProvider, FakeListLLM):
    id = "localai"
    name = "Local AI"
    model_id_key = "model"
    models = [
        "phi-2",
        "gpt-3.5-turbo"
    ]
    def __init__(self, **kwargs):
        model = kwargs.get("model_id")
        kwargs["responses"] = (
            ["This is a response from model 'phi-2'"]
            if model == "phi-2" else
            ["This is a response from model 'gpt-3.5-turbo'"]
        )
        super().__init__(**kwargs)

class LocalAIEmbeddingsProvider(BaseEmbeddingsProvider, FakeEmbeddings):
    id = "localai"
    name = "LocalAI Embeddings Provider"
    model_id_key = "model"
    models = ["awadb", "chromadb"]

    def __init__(self, **kwargs):
        super().__init__(size=300, **kwargs)