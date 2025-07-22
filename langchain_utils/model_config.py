# langchain_utils/model_config.py

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()  # Load .env file automatically

def get_llm_model(temperature: float = 1):
    model_name = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    api_key = os.getenv("OPENAI_API_KEY")

    return ChatOpenAI(
        model_name=model_name,
        temperature=temperature,
        openai_api_key=api_key
    )
