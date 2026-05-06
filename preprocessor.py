import re
from collections import Counter

class TextPreprocessor:
    def __init__(self):
        # 한글, 숫자, 영어, 기본 문장부호만 허용
        self.pattern = re.compile(r'[^ㄱ-ㅎㅏ-ㅣ가-힣a-zA-Z0-9\s.,!?]')
        # 자음/모음 반복 축약 패턴 (3번 이상 반복되면 2개로)
        self.repeat_pattern = re.compile(r'([ㄱ-ㅎㅏ-ㅣ])\1{2,}')
        # 최대 허용 글자 수
        self.max_length = 1000

    def _clean_noise(self, text: str) -> str:
        """기본 노이즈 제거 및 공백 정규화"""
        text = self.pattern.sub('', text)
        return " ".join(text.split())
    
    def _shrink_repeats(self, text: str) -> str:
        """과도한 자음/모음 반복 축약 (예: ㅋㅋㅋㅋㅋ -> ㅋㅋ) (Private)"""
        return self.repeat_pattern.sub(r'\1\1', text)
    
    def _truncate(self, text: str) -> str:
        """최대 글자 수 제한 (Private)"""
        if len(text) > self.max_length:
            return text[:self.max_length]
        return text
    
    def _is_meaningless(self, text: str) -> bool:
        """의미 없는 문장인지 통계적으로 판별"""
        if not text: return True

        # 1. 특정 글자의 과도한 점유율 체크 (예: "아아아아아")
        char_counts = Counter(text.replace(" ", "")) # 공백 제외 글자수 세기
        if char_counts:
            most_common_char, count = char_counts.most_common(1)[0]
            if count / len(text.replace(" ", "")) > 0.7: # 한 글자가 70% 이상이면 의미 없음
                return True

        # 2. 자모음(ㄱ, ㄴ, ㅏ)의 비율 체크
        pure_jamo = len(re.findall(r'[ㄱ-ㅎㅏ-ㅣ]', text))
        total_len = len(text.replace(" ", ""))
        if pure_jamo / total_len > 0.5: # 자모음이 절반 이상이면 의미 없음
            return True

        # 3. 단순 나열형 패턴 (가나다라마...) 체크는 사실 LLM이 더 잘하지만, 
        # 여기서는 글자 종류의 다양성으로 체크 가능
        if len(set(text.replace(" ", ""))) < 3 and len(text) > 10:
            return True # 10자가 넘는데 사용된 글자가 2종류 이하인 경우
    
    def _is_valid(self, text: str) -> tuple[bool, str]:
        """유효성 검사 및 사유 반환"""
        if not text:
            return False, "Empty Text"
        if len(text) < 5:
            return False, f"Too Short ({len(text)}자)"
        if not re.search(r'[가-힣]', text):
            return False, "No Korean Content"
        if self._is_meaningless(text):
            return False, "Meaningless Pattern (의미 없는 반복/나열)"
        return True, "Success"
    

    def run(self, raw_text: str) -> tuple[str | None, str]:
        """
        전체 파이프라인 실행
        반환: (전처리된 텍스트, 상태 메시지)
        """
        # 자르기
        text = self._truncate(raw_text)
        # 노이즈 제거
        text = self._clean_noise(text)
        # 반복 축약
        text = self._shrink_repeats(text)
        # 최종 유효성 검사
        is_ok, message = self._is_valid(text)
        
        if not is_ok:
            return None, message
            
        return text, message
    

if __name__ == "__main__":
    preprocessor = TextPreprocessor()
    
    print("="*50)
    print("NLP 전처리 모듈 테스트 모드 (종료하려면 'exit' 입력)")
    print("="*50)

    while True:
        user_input = input("\n분석할 일기 내용을 입력하세요: ")
        
        if user_input.lower() in ['exit']:
            break
            
        result, status = preprocessor.run(user_input)
        
        print(f"[결과]: {result}")
        print(f"[상태]: {status}")