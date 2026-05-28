import asyncio
import os
import time
from typing import Any, List, Optional, Type

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field, create_model

from app.core.exceptions import LLMTimeoutException
from app.core.logger import get_logger
from nlp.llm_strategy import LLMProviderStrategy
from nlp.preprocessor import TextPreprocessor

load_dotenv()

logger = get_logger(__name__)


class HealthDataExtractor:
    def __init__(self, strategy: LLMProviderStrategy, metadata: dict):
        # 주입받은 LLM 전략을 사용하여 모델 빌드
        self.llm = strategy.create_model()
        self.preprocessor = TextPreprocessor()
        self.metadata = metadata
        self.target_fields = list(metadata.keys())

        self.system_prompt = (
            "너는 사용자의 일기 본문을 정밀하게 분석하여 당일의 라이프스타일 및 건강 행동 지표를 추출하는 보건 의료 전문가야.\n"
            "사용자가 작성한 '오늘 하루의 일기 내용'을 읽고, 주어지는 각 항목(fields)의 기준과 설명(description)을 바탕으로 해당 행동이나 상태가 감지되었는지 판별해줘.\n\n"
            "응답 시 주의사항:\n"
            "1. 모든 추출 항목의 타입은 '정수(int)'야.\n"
            "2. 오늘 일기 내용에서 해당 라이프스타일, 행위, 통증 호소 등이 명백히 '감지/급되었거나 유추' 가능하다면 값으로 1을 부여해.\n"
            "3. 일기 내용에 언급이 없거나 해당하지 않는다면 반드시 0을 부여해.\n"
            "4. 절대로 마음대로 추정 수치(g, kcal 등)를 지어내지 말고, 각 필드의 설명에 적힌 대로 오직 감지 여부(1 또는 0)만 판단해.\n\n"
            "분석 및 추출 항목: {fields}"
        )

    def _create_dynamic_pydantic_model(self) -> Type[BaseModel]:
        """
        입력받은 필드 리스트를 바탕으로 객체를 동적으로 생성
        """
        # 모든 필드를 Optional한 문자열 타입으로 정의합니다.
        field_definitions = {}
        for field in self.target_fields:
            config = self.metadata[field]
            f_type = config.get("type", Optional[str])
            f_desc = config.get("description", f"{field} 정보")
            field_definitions[field] = (f_type, Field(None, description=f_desc))

        # 'DynamicHealthData'라는 이름의 클래스를 런타임에 생성합니다.
        return create_model("DynamicHealthData", **field_definitions)

    def _generate_prompt(self, diary_text: str, target_fields: List[str]) -> List:
        prompt_template = ChatPromptTemplate.from_messages(
            [("system", self.system_prompt), ("user", "일기 내용: {input_text}")]
        )
        fields_str = ", ".join(target_fields)
        return prompt_template.format_messages(fields=fields_str, input_text=diary_text)

    async def extract(self, diary_text: str) -> Any:
        """
        실제로 LLM에 요청을 보내고 구조화된 객체를 반환 (Public)
        """
        start_time = time.perf_counter()

        # 1. 동적으로 응답 형식을 정의
        dynamic_model = self._create_dynamic_pydantic_model()

        # 2. LLM에게 응답 형식 강제
        structured_llm = self.llm.with_structured_output(dynamic_model)

        # 3. 프롬프트 생성
        processed_diary, status = self.preprocessor.run(diary_text)
        if processed_diary is None:
            logger.error(f"로그: 전처리 실패 - {status}")
            return None

        messages = self._generate_prompt(processed_diary, self.target_fields)

        # 4. 실제 호출 및 결과 반환
        try:
            logger.info(f"LLM 요청 시작 (입력 길이: {len(diary_text)})")

            result = await structured_llm.ainvoke(messages)

            end_time = time.perf_counter()
            duration = end_time - start_time

            logger.info(f"LLM 분석 완료 - 소요 시간: {duration:.2f}s")
            return result

        except asyncio.TimeoutError as e:
            logger.error(f"LLM 분석 중 에러 발생: {str(e)}")
            raise LLMTimeoutException()


def get_extractor() -> HealthDataExtractor:
    from nlp.llm_providers import GeminiProvider, OpenAIProvider
    from nlp.schema_config import HEALTH_METADATA

    provider_type = os.getenv("LLM_PROVIDER", "GEMINI").upper()

    if provider_type == "GEMINI":
        strategy = GeminiProvider()
    elif provider_type == "OPENAI":
        strategy = OpenAIProvider()
    else:
        raise ValueError(f"Unknown provider: {provider_type}")

    return HealthDataExtractor(strategy, metadata=HEALTH_METADATA)
