from jupyter_ai_magics import BaseProvider
from jupyter_ai_magics.providers import EnvAuthStrategy, TextField
from langchain_openai import ChatOpenAI, AzureChatOpenAI
from langchain_community.chat_models import ChatOllama

from jupyter_ai_magics import BaseEmbeddingsProvider
from langchain_community.embeddings import OllamaEmbeddings
from langchain_openai.embeddings import AzureOpenAIEmbeddings, OpenAIEmbeddings

import os

class DIVEChat(ChatOpenAI):
    def __init__(self, **kwargs):
        super().__init__(
            **kwargs, 
            base_url=os.environ.get("CHAT_BASE_URL") or "http://localhost:8000/v1", 
            api_key=os.environ.get("DIVE_API_KEY") or "_"
        )

class DIVEChatProvider(BaseProvider, DIVEChat):
    id = "dive"
    name = " DIVE"
    models = ['chat']
    model_id_key = "model_name"
    pypi_package_deps = ["langchain_openai"]

class DIVEEmbeddings(OpenAIEmbeddings):
    def __init__(self, **kwargs):
        super().__init__(
            **kwargs,
            base_url=os.environ.get("EMBED_BASE_URL") or "http://localhost:8000/v1",
            api_key=os.environ.get("DIVE_API_KEY") or "_"
        )

class DIVEEmbeddingsProvider(BaseEmbeddingsProvider, DIVEEmbeddings):
    id = "dive"
    name = " DIVE"
    models = ["embed"]
    model_id_key = "model"
    pypi_package_deps = ["langchain_openai"]

class DIVEChatOpenAI(ChatOpenAI):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class DIVEChatOpenAIProvider(BaseProvider, DIVEChatOpenAI):
    id = "dive-openai"
    name = " DIVE OpenAI"
    models = ['*']
    model_id_key = "model_name"
    model_id_label = "Model name"
    pypi_package_deps = ["langchain_openai"]
    registry = True
    fields = [
        TextField(key="base_url", label="Base URL (required)", format="text"),
    ]
    auth_strategy = EnvAuthStrategy(
        name="OPENAI_API_KEY", keyword_param="api_key"
    )    
    
class DIVEAzureChatOpenAI(AzureChatOpenAI):
    def __init__(self, **kwargs):
        super().__init__(
            **kwargs,
            azure_endpoint="https://apim-aoai-eas-dev02.azure-api.net/cs-eastus",
            openai_api_version="2024-02-01"
        )

class DIVEAzureChatOpenAIProvider(BaseProvider, DIVEAzureChatOpenAI):
    id = "dive-azure"
    name = " DIVE Azure"
    models = [
        "gpt4o",
    ]
    model_id_key = "azure_deployment"
    pypi_package_deps = ["langchain_openai"]
    # # Confusingly, langchain uses both OPENAI_API_KEY and AZURE_OPENAI_API_KEY for azure
    # # https://github.com/langchain-ai/langchain/blob/f2579096993ae460516a0aae1d3e09f3eb5c1772/libs/partners/openai/langchain_openai/llms/azure.py#L85
    auth_strategy = EnvAuthStrategy(
        name="AZURE_OPENAI_API_KEY", keyword_param="openai_api_key"
    )

class DIVEChatOllamaProvider(BaseProvider, ChatOllama):
    id = "dive-ollama"
    name = " DIVE Ollama"
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
    model_id_key = "model"
    pypi_package_deps = ["langchain_community"]

class DIVEOllamaEmbeddingsProvider(BaseEmbeddingsProvider, OllamaEmbeddings):
    id = "dive-ollama"
    name = " DIVE Ollama"
    models = [
        "all-minilm",
        "snowflake-arctic-embed",
        "nomic-embed-text",
        "mxbai-embed-large",
    ]
    model_id_key = "model"
    pypi_package_deps = ["langchain_community"]


class DIVEAzureOpenAIEmbeddings(AzureOpenAIEmbeddings):
    def __init__(self, **kwargs):
        super().__init__(
            **kwargs,
            azure_endpoint="https://apim-aoai-eas-dev02.azure-api.net/cs-eastus",
            openai_api_version="2024-02-01"
        )

class DIVEAzureOpenAIEmbeddingsProvider(BaseEmbeddingsProvider, DIVEAzureOpenAIEmbeddings):
    id = "dive-azure"
    name = " DIVE Azure"
    models = [
        "text-embedding-3-large"
    ]
    model_id_key = "model"
    pypi_package_deps = ["langchain_openai"]
    auth_strategy = EnvAuthStrategy(
        name="AZURE_OPENAI_API_KEY", keyword_param="openai_api_key"
    )