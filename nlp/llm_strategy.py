from abc import ABC, abstractmethod
from typing import Any, Dict
from langchain_core.language_models.chat_models import BaseChatModel

class LLMProviderStrategy(ABC):

    DEFAULT_CONFIG = {
        "temperature": 0,
        "request_timeout": 15.0
    }

    def _get_config(self, **kwargs) -> Dict[str, Any]:
        """기본 설정에 모델별 특화 설정 병합 메서드"""
        config = self.DEFAULT_CONFIG.copy()
        config.update(kwargs)
        return config

    """LLM 공급자별 모델 생성 추상 메서드"""
    @abstractmethod
    def create_model(self) -> BaseChatModel:
        pass