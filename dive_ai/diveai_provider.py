from jupyter_ai_magics import BaseProvider
from langchain.chat_models import ChatOpenAI


class ChatDIVEAI(ChatOpenAI):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, openai_api_base="https://dive.cs.cityu.edu.hk/ai/v1/", openai_api_key="123")

class ChatDIVEAIProvider(BaseProvider, ChatDIVEAI):
    id = "diveai-chat"
    name = "DIVE"
    models = [
        "mistral",
    ]
    model_id_key = "model_name"
    pypi_package_deps = ["openai"]
    # auth_strategy = EnvAuthStrategy(name="OPENAI_API_KEY")