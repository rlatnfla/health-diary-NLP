import os
from dotenv import load_dotenv
from extractor import get_extractor

load_dotenv()

def test_extract():

    try:
        extractor = get_extractor()
        print(f"로그: 주입된 모델 정보 -> {extractor.llm}")

        test_diary = "오늘 점심에 치즈버거 세트 하나 먹었어. 저녁엔 가볍게 샐러드 먹고 40분 정도 런닝했고 총 5km 뛰었어."
    

        result = extractor.extract(test_diary)

        print("\n" + "="*30)
        print("--- 최종 추출 결과 (객체 형태) ---")
        print(result)
        print("="*30 + "\n")

    except Exception as e:
        print(f"\n 테스트 중 오류 발생: {e}")

if __name__ == "__main__":
    test_extract()