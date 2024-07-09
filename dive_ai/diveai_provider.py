from jupyter_ai_magics import BaseProvider
from jupyter_ai_magics.providers import TextField, EnvAuthStrategy
from langchain_openai import ChatOpenAI, AzureChatOpenAI

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

class AzureChatDIVEAI(AzureChatOpenAI):
    def __init__(self, **kwargs):
        super().__init__(
            **kwargs,
            azure_endpoint="https://apim-aoai-eas-dev02.azure-api.net/cs-northcentralus",
            openai_api_version="2024-02-01"
        )

class AzureChatDIVEAIProvider(BaseProvider, AzureChatDIVEAI):
    id = "diveai-azure"
    name = "AI Azure"
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
    pypi_package_deps = ["openai", "langchain_openai"]
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
