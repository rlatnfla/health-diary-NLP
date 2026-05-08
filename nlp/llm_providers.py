from nlp.llm_strategy import LLMProviderStrategy
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

class GeminiProvider(LLMProviderStrategy):
    def create_model(self) -> ChatGoogleGenerativeAI:
        return ChatGoogleGenerativeAI(
            model="models/gemini-flash-latest",
            **self._get_config()
        )

class OpenAIProvider(LLMProviderStrategy):
    def create_model(self) -> ChatOpenAI:
        return ChatOpenAI(
            model="",
            **self._get_config(timeout=20.0)
        )