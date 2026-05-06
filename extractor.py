import os
from typing import List, Optional, Type, Any
from dotenv import load_dotenv
from pydantic import create_model, Field, BaseModel 
from llm_strategy import LLMProviderStrategy
from langchain_core.prompts import ChatPromptTemplate
from preprocessor import TextPreprocessor

load_dotenv()

class HealthDataExtractor:
    def __init__(self, strategy: LLMProviderStrategy, metadata: dict):
        # 주입받은 LLM 전략을 사용하여 모델 빌드
        self.llm = strategy.create_model()
        self.preprocessor = TextPreprocessor()
        self.metadata = metadata
        self.target_fields = list(metadata.keys())

        self.system_prompt = (
            "너는 사용자의 건강 일기를 분석하여 특정 지표를 수치화하는 보건 의료 전문가야.\n"
            "사용자의 입력 내용에서 정보를 추출하고, 만약 수치가 명시되지 않았다면 보건 의료 지식을 바탕으로 '추정치'를 계산해줘.\n"
            "응답 시 주의사항:\n"
            "1. 지방섭취량: 음식명만 적지 말고, 해당 음식의 일반적인 지방 함량을 'g' 단위 숫자로 추정해서 답해.\n"
            "2. 운동량: 운동 거리나 시간만 적지 말고, 일반적인 성인 기준 'kcal' 소모량을 계산해서 숫자로 답해.\n"
            "3. 모든 수치는 가급적 숫자 위주로 표현해줘.\n"
            "추출 및 분석 항목: {fields}"
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
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("user", "일기 내용: {input_text}")
        ])
        fields_str = ", ".join(target_fields)
        return prompt_template.format_messages(fields=fields_str, input_text=diary_text)

    def extract(self, diary_text: str) -> Any:
        """
        실제로 LLM에 요청을 보내고 구조화된 객체를 반환 (Public)
        """
        # 1. 동적으로 응답 형식을 정의
        dynamic_model = self._create_dynamic_pydantic_model()
        
        # 2. LLM에게 응답 형식 강제
        structured_llm = self.llm.with_structured_output(dynamic_model)
        
        # 3. 프롬프트 생성
        processed_diary, status = self.preprocessor.run(diary_text)
        if processed_diary is None:
            print(f"로그: 전처리 실패 - {status}")
            return None
        
        messages = self._generate_prompt(processed_diary, self.target_fields)
        
        # 4. 실제 호출 및 결과 반환
        return structured_llm.invoke(messages)

def get_extractor() -> HealthDataExtractor:
        from llm_providers import GeminiProvider, OpenAIProvider
        from schema_config import HEALTH_METADATA

        provider_type = os.getenv("LLM_PROVIDER", "GEMINI").upper()
    
        if provider_type == "GEMINI":
            strategy = GeminiProvider()
        elif provider_type == "OPENAI":
            strategy = OpenAIProvider()
        else:
            raise ValueError(f"Unknown provider: {provider_type}")
            
        return HealthDataExtractor(strategy, metadata=HEALTH_METADATA)
