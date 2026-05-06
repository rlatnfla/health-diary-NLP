from abc import ABC, abstractmethod
from langchain_core.language_models.chat_models import BaseChatModel

class LLMProviderStrategy(ABC):
    """LLM 공급자별 모델 생성 추상 메서드"""
    @abstractmethod
    def create_model(self) -> BaseChatModel:
        pass