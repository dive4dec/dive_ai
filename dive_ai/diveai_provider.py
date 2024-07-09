from jupyter_ai_magics import BaseProvider
from langchain_community.chat_models import ChatOpenAI


# class ChatDIVEAI(ChatOpenAI):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs, openai_api_base="http://ai.local-ai/v1/", openai_api_key="123")

# class ChatDIVEAIProvider(BaseProvider, ChatDIVEAI):
#     id = "diveai-chat"
#     name = "AI"
#     models = [
#         "mistral",
#     ]
#     model_id_key = "model_name"
#     pypi_package_deps = ["openai"]
#     # auth_strategy = EnvAuthStrategy(name="OPENAI_API_KEY")

class ChatDIVEAI(ChatOpenAI):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, openai_api_base="http://localhost:11434/v1/", openai_api_key="123")

class ChatDIVEAIProvider(BaseProvider, ChatDIVEAI):
    id = "diveai"
    name = "AI"
    models = [
        "dolphin-mistral",
        "codestral",
        "starcoder2",
        "llava",
        "codegemma",
        "codeqwen",
        "mistral",
        "codellama",
        "aya",
        "deepseek-coder-v2",
        "phi3",
        "qwen2",
        "llama3",
        "gemma2",
    ]
    model_id_key = "model_name"
    pypi_package_deps = ["openai", "langchain_community"]
    # auth_strategy = EnvAuthStrategy(name="OPENAI_API_KEY")


from jupyter_ai_magics import BaseEmbeddingsProvider
from langchain_community.embeddings import OllamaEmbeddings

class DIVEAIEmbeddings(OllamaEmbeddings):
    pass

class DIVEAIEmbeddingsProvider(BaseEmbeddingsProvider, DIVEAIEmbeddings):
    id = "diveai"
    name = "AI"
    models = [
        "all-minilm",
        "snowflake-arctic-embed",
        "nomic-embed-text",
        "mxbai-embed-large",
    ]
    model_id_key = "model"
    pypi_package_deps = ["langchain_community"]
